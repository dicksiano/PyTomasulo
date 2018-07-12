class Register:
    def __init__(self, value, ready):
        self.value = value
        self.ready = ready

class Register_Status:
    def __init__(self):
        self.reg = {}
        for i in range(0,32):
            self.reg['R' + str(i)] = Register(0, True)
        self.reg['R1'].value = 4

    def get_status(self):
        status = []
        for i in range(0,32):            
            status.append(self.reg['R' + str(i)].value)
        return status

    def print_status(self):
        for i in range(0,32):
            print('R' + str(i) + ": " + str(self.reg['R' + str(i)].value), end=" ")

    def is_ready(self, reg):
        return self.reg[reg].ready

    def get_value(self, reg):
        return self.reg[reg].value

    def set_param(self, reg, value, ready):
        self.reg[reg].value = value
        self.reg[reg].ready = ready
    