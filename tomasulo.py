import instruction_set
import reservation_status
import register_status
import memory_model

# TODO clean exec unit when write, do Vj = Vk = Qj = Qk = none

class Tomasulo:
    def __init__(self, instruction_set):
        self.instruction_set = instruction_set
        self.reservation = reservation_status.Reservation_Status()
        self.registers = register_status.Register_Status()
        self.memory = memory_model.Memomy_Model()
        self.cycle = 0

    def update(self):
        self.cycle += 1

        self.write()
        self.execute()
        self.issue()

    # Takes the next instruction and Issue it.
    # Depends of what execution units are available
    # Only one instruction per cycle
    def issue(self):
        current_inst = self.instruction_set.get_next_instruction()

        if self.reservation.is_unit_available(current_inst.unit_type):
            self.instruction_set.update_PC()            

            exec_unit = self.reservation.get_exec_unit(current_inst.unit_type)
            current_inst.issue(exec_unit)
            exec_unit.Busy = True
            exec_unit.Op = current_inst.name

    # Take all issued instructions and try to execute them
    def execute(self):
        for i in self.instruction_set.all:
            if i.get_state() == 'issue':
                if i.type == 'rtype':
                    self.execute_rtype(i) 
                elif i.type == 'itype':
                    self.execute_itype(i)
                elif i.type == 'jtype':
                    self.execute_jtype(i)
                else:
                    raise Exception("Unknown type: " + i.type)
            if i.get_state() == 'exec':
                print(i.name + ' ' + str(i.cycles_execute))
                i.execute()

    # Take all instructions in execution. If the execution has finished, then write it
    def write(self):
        for i in self.instruction_set.all:
            if i.get_state() == 'exec' and i.cycles_execute <= 0:
                i.write()
                if i.type == 'rtype':
                    self.solve_rtype(i)
                elif i.type == 'itype':
                    self.solve_itype(i)
                elif i.type == 'jtype':
                    self.solve_jtype(i)

    def execute_rtype(self, inst):
        if inst.op == 'nop': # Nop doesn't need any register
            inst.execute()
        else:
            if inst.exec_unit.Vj == 'none':
                if self.registers.is_ready(inst.rs):
                    inst.exec_unit.Vj = self.registers.get_value(inst.rs) # Put register value at Vj
                else:
                    inst.exec_unit.Qj = self.registers.get_value(inst.rs)

            if inst.exec_unit.Vk == 'none':
                if self.registers.is_ready(inst.rt):
                    inst.exec_unit.Vk = self.registers.get_value(inst.rt) # Put register value at VK
                else:
                    inst.exec_unit.Qk = self.registers.get_value(inst.rt)
            
            if inst.exec_unit.Vj != 'none' and inst.exec_unit.Vk != 'none': # The op doesn't has dependencies
                self.registers.set_param(inst.rd, inst.name, False)
                inst.execute()

    def execute_itype(self, inst):        
        if inst.exec_unit.Vj == 'none':
            if self.registers.is_ready(inst.rs):
                inst.exec_unit.Vj = self.registers.get_value(inst.rs) # Put register value at Vj
        else:
            inst.exec_unit.Qj = self.registers.get_value(inst.rs)

        # Beq, Ble, Bne also need rt, but Addi just need rs
        if inst.op != 'Addi':
            if inst.exec_unit.Vk == 'none':
                if self.registers.is_ready(inst.rt):
                    inst.exec_unit.Vk = self.registers.get_value(inst.rt) # Put register value at VK
                else:
                    inst.exec_unit.Qk = self.registers.get_value(inst.rt)
        else:
            inst.exec_unit.Vk = inst.immediate
        
        if inst.exec_unit.Vj != 'none' and inst.exec_unit.Vk != 'none': # The op doesn't has dependencies
            if inst.op != 'Sw': # Sw: MEM[ rs +Immed ] = rt
                self.registers.set_param(inst.rt, inst.exec_unit.name, False) 
            inst.execute()

    def execute_jtype(self, inst):
        inst.execute()
    
    def render(self):
        print('\nCycle: ' + str(self.cycle))

        print('\nInstruction Set')
        print("         Op            Is    Exec   Wr  ")
        self.instruction_set.print_status()

        print('\nReservation Status')
        print("   Stat    Busy           Op            Vj     Vk     Qj     Qk     A     Res")
        self.reservation.print_status()

        print('\nRegister Status')
        self.registers.print_status()

    def solve_rtype(self, inst):
        if inst.type != 'Nop':
            if inst.op == 'Add':
                self.registers.set_param(inst.rd, inst.exec_unit.Vj + inst.exec_unit.Vk, True)
            elif inst.op == 'Sub':
                self.registers.set_param(inst.rd, inst.exec_unit.Vj - inst.exec_unit.Vk, True)
            elif inst.op == 'Mul':
                self.registers.set_param(inst.rd, inst.exec_unit.Vj * inst.exec_unit.Vk, True)
            else:
                raise Exception("Unknown rtype op: " + inst.op)

    def solve_itype(self, inst):        
        if inst.op == 'Addi':
            self.registers.set_param(inst.rt, inst.exec_unit.Vj + inst.exec_unit.Vk, True)
        elif inst.op == 'Beq':
            if inst.exec_unit.Vj == inst.exec_unit.Vk:
                self.instruction_set.update_PC(1 + inst.immediate)
        elif inst.op == 'Ble':
            if inst.exec_unit.Vj <= inst.exec_unit.Vk:
                self.instruction_set.update_PC(1 + inst.immediate)
        elif inst.op == 'Bne':
            if inst.exec_unit.Vj != inst.exec_unit.Vk:
                self.instruction_set.update_PC(1 + inst.immediate)
        elif inst.op == 'Lw':
            self.registers.set_param(inst.rt, self.memory.get(inst.exec_unit.Vj + inst.immediate), True)
        elif inst.op == 'Sw':
            self.memory.set(inst.immediate + inst.exec_unit.Vj, inst.exec_unit.Vk)
            self.registers.set_param(inst.rt, self.memory.get(inst.exec_unit.Vj + inst.immediate), True)
        else:
            raise Exception("Unknown itype op: *" + inst.op + '*')

    def solve_jtype(self, inst):
        self.instruction_set.update_PC(inst.target_adress)
    
