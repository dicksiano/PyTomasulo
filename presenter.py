import sys
sys.path.append('../model/')

import utils
import instruction_set
import tomasulo

class Presenter:
    def __init__(self):
        self.play = False
        input_inst = utils.read_input("test.txt") # Read input
        inst_set = instruction_set.Instruction_Set(input_inst)
        self.tomasulo_impl = tomasulo.Tomasulo(inst_set)

    def update(self):
        self.tomasulo_impl.update()
        #self.tomasulo_impl.render()
    
    def get_status(self):
        return self.tomasulo_impl.get_status()