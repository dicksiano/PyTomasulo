import utils
import instruction_set
import tomasulo

def main():
    input_inst = utils.read_input("test.txt")
    inst_set = instruction_set.Instruction_Set(input_inst)
    tomasulo_impl = tomasulo.Tomasulo(inst_set)

    while(1):
        input('play')
        tomasulo_impl.update()
        tomasulo_impl.render()

if __name__ == "__main__":
    main()