"""
	Class that represents a o model of an RType instruction
	"""
class Instruction:
	def __init__(self, op):
		self.state = 'queued'
		self.name = 'none'
		self.type = 'none'
		self.exec_unit = 'none'
		self.cycles_execute = 0

		if op in ['Add', 'Sub', 'Addi', 'Beq', 'Ble', 'Bne', 'Jmp']:
			self.unit_type = 'Add'
		elif op in ['Lw', 'Sw']:
			self.unit_type = 'Mem'
		elif op in ['Mul']:
			self.unit_type = 'Mul'
		else:
			raise Exception("Unknow unit type: " + op)

	def issue(self, exec_unit):
		self.state = 'issue'
		self.exec_unit = exec_unit

	def execute(self):
		self.state = 'exec'
		self.cycles_execute -= 1 # decrease the number of cycles to exec

	def write(self):
		self.state = 'write'
	
	def finalize(self):
		self.state = 'finished'
		
	def get_state(self):
		return self.state

	def get_type(self):
		return self.type

	def is_ready_to_exec(self):
		return self.exec_unit.Vj != 'none' and self.exec_unit.Vk != 'none'

	def get_status(self):
		return [self.name, self.state == 'issue', self.state == 'exec', self.state == 'write', self.state == 'finished']
		
	def print_status(self):
		print("%20s" %self.name + ' ' + "%6s" %str(self.state == 'issue') + ' ' + "%6s" %str(self.state == 'exec') + ' ' + "%6s" %str(self.state == 'write') + ' ' + "%6s" %str(self.state == 'finished'))


class RType_Instruction(Instruction):
	def __init__(self, op,rs,rt,rd):
		Instruction.__init__(self, op)
		self.type = 'rtype'
		self.op = op
		self.rs = rs
		self.rt = rt
		self.rd = rd
		self.name = op + ' ' + rd + ',' + rs + ',' + rt

		# Mul takes 3 cycle to execute and Add/Sub/Nop takes 1
		if op == 'Mul':
			self.cycles_execute = 3 
		else:
			self.cycles_execute = 1

class IType_Instruction(Instruction):
	def __init__(self, op, rs,rt,immediate):
		Instruction.__init__(self, op)
		self.type = 'itype'
		self.op = op
		self.rs = rs
		self.rt = rt
		self.immediate = int(immediate)

		# Lw,Sw takes 4 cycle to execute and Addi/Beq/Ble/Bne takes 1
		if op == 'Lw' or op == 'Sw':
			self.cycles_execute = 4 
			self.name = op + ' ' + rt + ',' + immediate + '(' + rs + ')'
		else:
			self.cycles_execute = 1
			self.name = op + ' ' + rt + ',' + rs + ',' + immediate

class JType_Instruction(Instruction):
	def __init__(self, opcode,target_adress):
		Instruction.__init__(self, opcode)
		self.type = 'jtype'
		self.op = opcode
		self.target_adress = target_adress
		self.name = opcode + ' ' + target_adress
		self.cycles_execute = 1
		