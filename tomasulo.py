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
        self.issued_instructions = 0
        # Only 1 type of operation per time:
        self.is_add_ready = True
        self.is_mult_ready = True
        self.is_mem_ready = True
        # Have to wait branch operations
        self.is_waiting_branch = False

    def update(self):
        if not self.has_finished():
            self.cycle += 1
            self.write()
            self.execute()
            self.issue()

    def get_status(self):
        return [ self.cycle, self.instruction_set.get_status(), self.reservation.get_status(), self.registers.get_status() ]

    # Takes the next instruction (one per cycle) and Issue it if possible. Depends of what execution units are available   
    def issue(self):
        if not self.instruction_set.is_finished() and not self.is_waiting_branch:
            current_inst = self.instruction_set.get_next_instruction() # Take the instruction that is pointed by PC

            if self.reservation.is_unit_available(current_inst.unit_type): # Check if there is execution unit available
                self.instruction_set.update_PC() # PC = PC + 1. Only updates PC if there is an available exec unit         
                self.issued_instructions += 1
                exec_unit = self.reservation.get_exec_unit(current_inst.unit_type) # Get the available exec unit
                current_inst.issue(exec_unit) # Instruction receive status 'issue' 
                exec_unit.Busy = True # Exec unit will be busy until process this instruction
                exec_unit.Op = current_inst.name # Set who is occuping the exec unit

                self.setup_exec(current_inst) # Setup: update Vj, Vk. If there are dependencies, then use Qj, Qk 
                
                if current_inst.op == 'Beq' or current_inst.op == 'Ble' or current_inst.op == 'Bne': # Branch operations
                    self.is_waiting_branch = True

    # Take all issued instructions and try to execute them
    def execute(self):
        for i in self.instruction_set.all:
            if i.get_state() == 'issue':
                if i.is_ready_to_exec(): # Dependencies have finished their execution
                    if i.unit_type == 'Add' and self.is_add_ready:
                        self.start_execution(i)
                        self.is_add_ready = False
                    if i.unit_type == 'Mul' and self.is_mult_ready:
                        self.start_execution(i)
                        self.is_mult_ready = False
                    if i.unit_type == 'Mem' and self.is_mem_ready:
                        self.start_execution(i)
                        self.is_mem_ready = False

            elif i.get_state() == 'exec':
                i.execute()          

    # Take all instructions in execution. If the execution has finished, then write it
    def write(self):
        for i in self.instruction_set.all:
            if i.get_state() == 'write':
                i.exec_unit.clear() # Free exec unit to others instructions be processed
                i.finalize()
            elif i.get_state() == 'exec' and i.cycles_execute <= 0:
                i.write()

                if i.unit_type == 'Add':
                        self.is_add_ready = True
                elif i.unit_type == 'Mul':
                        self.is_mult_ready = True
                elif i.unit_type == 'Mem':
                        self.is_mem_ready = True

                if i.type == 'rtype':
                    self.solve_rtype(i)
                elif i.type == 'itype':
                    self.solve_itype(i)
                elif i.type == 'jtype':
                    self.solve_jtype(i)

    def start_execution(self, inst):
        if inst.op == 'Nop' or inst.type == 'jtype': # Nop, Jmp doesn't need any register
            inst.execute()
        else:
            if inst.type == 'rtype':
                self.registers.set_param(inst.rd, inst.exec_unit.name, False) # Lock rd register. It can be overwriten by the next instructions
                inst.execute()
            elif inst.type == 'itype':
                if inst.op == 'Addi' or inst.op == 'Lw': # Addi and Lw use rt to storage the result. All other itype op don't
                    self.registers.set_param(inst.rt, inst.exec_unit.name, False)  # Lock rt register. It can be overwriten by the next instructions
                inst.execute()

    def setup_exec(self, inst):        
        if inst.op == 'nop' or inst.type == 'jtype':
            inst.exec_unit.Vj = '-'
            inst.exec_unit.Vk = '-'
        else:
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

            if inst.exec_unit.name == self.registers.get_value(inst.rd): # JUST write if rd is waiting for this op
                self.registers.set_param(inst.rd, result, True) # write value to rd
            self.reservation.bypass(inst.exec_unit.name, result) # Bypass the result 
            inst.exec_unit.A = result

    def solve_itype(self, inst):        
        if inst.op == 'Beq':
            self.is_waiting_branch = False # Finish of branch op
            if inst.exec_unit.Vj == inst.exec_unit.Vk:
                self.instruction_set.update_PC(1 + inst.immediate)
        elif inst.op == 'Ble':
            self.is_waiting_branch = False # Finish of branch op
            if inst.exec_unit.Vj <= inst.exec_unit.Vk:
                self.instruction_set.update_PC(1 + inst.immediate)
        elif inst.op == 'Bne':
            self.is_waiting_branch = False # Finish of branch op
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

            if inst.exec_unit.name == self.registers.get_value(inst.rt): # JUST write if rt is waiting for this op
                self.registers.set_param(inst.rt, result, True) # Write value to register
            self.reservation.bypass(inst.exec_unit.name, result) # Bypass the result 
            inst.exec_unit.A = result
        else:
            raise Exception("Unknown itype op: *" + inst.op + '*')

    def solve_jtype(self, inst):
        self.instruction_set.set_PC(inst.target_adress)

    def has_finished(self):
        return all(i.get_state() == 'finished' for i in self.instruction_set.all)
    
