import instructions
"""
	RType instructions are defined by the field Funct
  """
Rtype_dic = {
			"100000": "Add",
			"011000": "Mul",
			"000000": "Nop",
			"100010": "Sub"
	}

"""
	IType instructions are defined by their OPcode
  """
IType_dic = {
			"001000": "Addi",
			"000101": "Beq", 
			"000111": "Ble",
			"000100": "Bne",
			"100011": "Lw",
			"101011": "Sw"
}

"""
	JType is built by only one op: Sw "101011" 
	"""
JType_dic = {
	"000010": "Jmp"
}

def is_RType(opcode):
	return opcode == "000000"
def is_JType(opcode):
	return opcode == "000010"
def is_IType(opcode):
	return (not is_RType(opcode)) and (not is_JType(opcode))


def parse_RType(instruction):
	opcode = instruction[0:6]
	rs = instruction[6:11]
	rt = instruction[11:16]
	rd = instruction[16:21]
	shamt = instruction[21:26]
	funct = instruction[26:32]

	return [opcode,rs,rt,rd,shamt,funct]

def parse_IType(instruction):
	opcode = instruction[0:6]
	rs = instruction[6:11]
	rt = instruction[11:16]
	immediate = instruction[16:32]

	return [opcode,rs,rt,immediate]

def parse_JType(instruction):	
	opcode = instruction[0:6]
	target_adress = instruction[6:32]

	return [opcode,target_adress]

def decode_reg(b):
	return 'R' + str(int(b,2))


def decode_RType(opcode,rs,rt,rd,shamt,funct):
	op = Rtype_dic[funct] # Rtype instructions are defined by FUNCT
	rs = decode_reg(rs)
	rt = decode_reg(rt)
	rd = decode_reg(rd)

	return [op,rs,rt,rd]


def decode_IType(opcode, rs, rt, immediate):
	op = IType_dic[opcode]
	rs = decode_reg(rs)
	rt = decode_reg(rt)
	immediate = str(int(immediate,2))

	return [op, rs,rt,immediate]

def decode_JType(opcode,target_adress):
	op = JType_dic[opcode]
	target_adress = str(int(target_adress,2))

	return [op,target_adress]

def parse_instruction(instruction):
	opcode = instruction[0:6]
	
	if(is_RType(opcode)):
		[opcode,rs,rt,rd,shamt,funct] = parse_RType(instruction)
		[op,rs,rt,rd] = decode_RType(opcode,rs,rt,rd,shamt,funct)
		return instructions.RType_Instruction(op,rs,rt,rd)

	elif(is_JType(opcode)): 
		[opcode,target_adress] = parse_JType(instruction)
		[opcode,target_adress] = decode_JType(opcode,target_adress)
		return instructions.JType_Instruction(opcode,target_adress)

	elif(is_IType(opcode)):
		[opcode,rs,rt,immediate] = parse_IType(instruction)
		[opcode,rs,rt,immediate] = decode_IType(opcode,rs,rt,immediate)
		return instructions.IType_Instruction(opcode,rs,rt,immediate)

	else:
		raise Exception("Unkown instruction: " + instruction)

def read_input(input):
	file = open(input)
	input = file.read().splitlines()
	
	instructions = []
	for line in input:
		instructions.append(parse_instruction(line))
	return instructions

