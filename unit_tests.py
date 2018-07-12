import utils
import instructions
import instruction_set

"""
    Utils unit tests
    """
 
assert utils.is_RType("000000") == True
assert utils.is_RType("000100") == False
assert utils.is_JType("000010") == True
assert utils.is_JType("111111") == False

assert utils.parse_RType("00100000000010100000000001100100") == ['001000', '00000', '01010', '00000', '00001', '100100']
assert utils.parse_IType("00100000000010100000000001100100") == ['001000', '00000', '01010', '0000000001100100']
assert utils.parse_JType("00100000000010100000000001100100") == ['001000', '00000010100000000001100100']

assert utils.parse_RType("00000000110001100011100000011000") == ['000000','00110','00110','00111','00000','011000']
assert utils.decode_RType('000000','00110','00110','00111','00000','011000') == ['Mul','R6','R6','R7']

assert utils.parse_IType("00100000000010100000000001100100 ") == ['001000','00000','01010','0000000001100100']
assert utils.decode_IType('001000','00000','01010','0000000001100100') == ['Addi','R0','R10','100']

assert utils.parse_JType("00001000000000000000000000011000") == ['000010','00000000000000000000011000']
assert utils.decode_JType('000010','00000000000000000000011000') == ['Jmp','24']

assert utils.parse_instruction("00100000000010100000000001100100") == instructions.IType_Instruction('Addi', 'R0', 'R10', '100')
assert utils.parse_instruction("00001000000000000000000000011000") == ['Jmp', '24']
assert utils.parse_instruction("00001000000000000000000000011100") == ['Jmp', '28']

assert utils.read_input('test.txt') == [
									['Addi', 'R0', 'R10', '100'], 
									['Sw', 'R0', 'R0', '24'], 
									['Sw', 'R0', 'R0', '28'], 
									['Lw', 'R0', 'R6', '28'], 
									['Mul', 'R6', 'R6', 'R7'], 
									['Lw', 'R0', 'R1', '24'], 
									['Add', 'R1', 'R7', 'R9'], 
									['Sw', 'R0', 'R9', '24'], 
									['Addi', 'R6', 'R6', '1'], 
									['Sw', 'R0', 'R6', '28'], 
									['Ble', 'R6', 'R10', '20']
								]

"""
    Instruction set unit tests
    """
instrA = instructions.RType_Instruction('Add','R0','R1','R2')
instrA.finalize()
instrB = instructions.IType_Instruction('Ble','R0','R1','100')
instrB.finalize()
instrC = instructions.JType_Instruction('Sw','30')
instrC.finalize()

instrD = instructions.RType_Instruction('Add','R7','R7','R7')
instrE = instructions.IType_Instruction('Addi','R7','R7','7')
instrF = instructions.JType_Instruction('Sw','7')

instruc = [instrA,instrB,instrC,instrD,instrE,instrF]
inst_set = instruction_set.Instruction_Set(instruc)
inst_set.update()

print('\nnot f')
for instruction in inst_set.not_finalized:
    print(instruction.name)

print('\nfin')
for instruction in inst_set.finalized:
    print(instruction.name)

print('\n\n')
print(inst_set.first_rtype().name)
print(inst_set.first_itype().name)
print(inst_set.first_jtype().name)