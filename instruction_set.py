import instructions

class Instruction_Set:
    def __init__(self, instructions):
        self.all = instructions
        self.program_counter = 0

    def get_next_instruction(self):
        return self.all[self.program_counter]

    def update_PC(self, offset=1):
        self.program_counter += offset

    def print_status(self):
        for i in self.all:
            i.print_status()

    def is_finished(self):
        return self.program_counter >= len(self.all)

    def get_status(self):
        status = []
        for i in self.all:
            status.append(i.get_status())
        return status

