import instruction_set
import reservation_status
import register_status
import memory_model

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

    def get_status(self):
        return [
                self.instruction_set.get_status(),
                self.reservation.get_status(),
                self.registers.get_status()
                ]

    # Takes the next instruction (one per cycle) and Issue it if possible. Depends of what execution units are available   
    def issue(self):
        if not self.instruction_set.is_finished():
            current_inst = self.instruction_set.get_next_instruction() # Take the instruction that is pointed by PC

            if self.reservation.is_unit_available(current_inst.unit_type): # Check if there is execution unit available
                self.instruction_set.update_PC() # PC = PC + 1           

                exec_unit = self.reservation.get_exec_unit(current_inst.unit_type) # Get the available exec unit
                current_inst.issue(exec_unit) # Instruction receive status 'issue' 
                exec_unit.Busy = True # Exec unit will be busy until process this instruction
                exec_unit.Op = current_inst.name 

    # Take all issued instructions and try to execute them
    def execute(self):
        for i in self.instruction_set.all:
            if i.get_state() == 'exec':
                i.execute()
            elif i.get_state() == 'issue':
                if i.is_ready_to_exec(): # Dependencies have finished their execution
                    i.execute()
                elif not i.is_waiting_dependencies(): # Has not passed through set up
                    if i.type == 'rtype':
                        self.execute_rtype(i) 
                    elif i.type == 'itype':
                        self.execute_itype(i)
                    elif i.type == 'jtype':
                        self.execute_jtype(i)
                    else:
                        raise Exception("Unknown type: " + i.type)            

    # Take all instructions in execution. If the execution has finished, then write it
    def write(self):
        for i in self.instruction_set.all:
            if i.get_state() == 'write':
                i.exec_unit.clear() # Free exec unit to others instructions be processed
                i.finalize()
            elif i.get_state() == 'exec' and i.cycles_execute <= 0:
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
            self.setup_exec(inst) # Setup: update Vj, Vk. If there are dependencies, then use Qj, Qk            
            if inst.is_ready_to_exec(): # The op doesn't have any dependencies
                self.registers.set_param(inst.rd, inst.name, False) # Lock rd register
                inst.execute()

    def execute_itype(self, inst):
        self.setup_exec(inst) # Setup: update Vj, Vk. If there are dependencies, then use Qj, Qk  
        if inst.is_ready_to_exec(): # The op doesn't have any dependencies
            if inst.op == 'Addi' or inst.op == 'Lw': # Addi and Lw use rt to storage the result. All other itype op don't
                self.registers.set_param(inst.rt, inst.exec_unit.name, False)  # Lock rt register
            inst.execute()

    def setup_exec(self, inst):        
        if self.registers.is_ready(inst.rs):
            inst.exec_unit.Vj = self.registers.get_value(inst.rs) # Put register value at Vj
        else:
            inst.exec_unit.Qj = self.registers.get_value(inst.rs) # Waiting for dependencies

        if inst.op != 'Addi' and inst.op != 'Lw': # Add, Sub, Mul, Beq, Ble, Bne, Sw also need rt
            if self.registers.is_ready(inst.rt):
                inst.exec_unit.Vk = self.registers.get_value(inst.rt) # Put register value at Vk
            else:
                inst.exec_unit.Qk = self.registers.get_value(inst.rt) # Waiting for dependencies
        else:
            inst.exec_unit.Vk = inst.immediate

    def execute_jtype(self, inst):
        inst.execute() # Jmp doesn't need any register
    
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
                result = inst.exec_unit.Vj + inst.exec_unit.Vk
            elif inst.op == 'Sub':
                result = inst.exec_unit.Vj - inst.exec_unit.Vk
            elif inst.op == 'Mul':
                result = inst.exec_unit.Vj * inst.exec_unit.Vk
            else:
                raise Exception("Unknown rtype op: " + inst.op)

            self.registers.set_param(inst.rd, result, True) # write value to rd
            self.reservation.bypass(inst.exec_unit.name, result) # Bypass the result 

    def solve_itype(self, inst):        
        if inst.op == 'Beq':
            if inst.exec_unit.Vj == inst.exec_unit.Vk:
                self.instruction_set.update_PC(1 + inst.immediate)
        elif inst.op == 'Ble':
            if inst.exec_unit.Vj <= inst.exec_unit.Vk:
                self.instruction_set.update_PC(1 + inst.immediate)
        elif inst.op == 'Bne':
            if inst.exec_unit.Vj != inst.exec_unit.Vk:
                self.instruction_set.update_PC(1 + inst.immediate)
        elif inst.op == 'Sw':
            self.memory.store_in_memory(inst.immediate + inst.exec_unit.Vj, inst.exec_unit.Vk)
        # Addi and Lw has to do Bypass
        elif inst.op == 'Addi' or inst.op == 'Lw':
            if inst.op == 'Addi':
                result = inst.exec_unit.Vj + inst.exec_unit.Vk
            elif inst.op == 'Lw':
                result = self.memory.load_from_memory(inst.exec_unit.Vj + inst.exec_unit.Vk)

            self.registers.set_param(inst.rt, result, True) # Write value to register
            self.reservation.bypass(inst.exec_unit.name, result) # Bypass the result 
        else:
            raise Exception("Unknown itype op: *" + inst.op + '*')

    def solve_jtype(self, inst):
        self.instruction_set.update_PC(inst.target_adress)
    
