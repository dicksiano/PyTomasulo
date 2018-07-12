""" 
    Class that represents a single Execution Unit
    """
class Execution_Unit:
    def __init__(self, name):
        self.name = name
        self.Busy = False
        self.Op = 'none'
        self.Vj = 'none'
        self.Vk = 'none'
        self.Qj = 'none'
        self.Qk = 'none'
        self.A = 'none'
        self.Result = 'none'

    def is_busy(self):
        return self.is_busy

    def get_all(self):
        return [self.name, 
                self.Busy, 
                self.Op, 
                self.Vj, 
                self.Vk, 
                self.Qj, 
                self.Qk, 
                self.A, 
                self.Result]

    def print_status(self):
        print("%7s: " %self.name + "%6s" %self.Busy + ' ' + "%20s" %self.Op + ' ' + "%6s" %self.Vj + ' ' + "%6s" %self.Vk + ' ' + "%6s" %self.Qj + ' ' + "%6s" %self.Qk + ' ' + "%6s" %self.A + ' ' + "%6s" %self.Result)

class Reservation_Status:
    def __init__(self):
        self.load0 = Execution_Unit("load0")
        self.load1 = Execution_Unit("load1")
        self.add0 = Execution_Unit("add0")
        self.add1 = Execution_Unit("add1")
        self.add2 = Execution_Unit("add2")
        self.mult0 = Execution_Unit("mult0")
        self.mult1 = Execution_Unit("mult1")

    def print_status(self):
        self.load0.print_status()
        self.load1.print_status()
        self.add0.print_status()
        self.add1.print_status()
        self.add2.print_status()
        self.mult0.print_status()
        self.mult1.print_status()

    def is_unit_available(self, type):
        if type == 'Add':
            return self.is_add_available()
        elif type == 'Mem':
            return self.is_load_available()
        elif type == 'Mul':
            return self.is_mul_available()
        else:
            raise Exception('Unkown unit type: ' + type)

    def get_exec_unit(self, type):
        if(self.is_unit_available(type)):
            if type == 'Add':
                if not self.add0.Busy:
                    return self.add0
                elif not self.add1.Busy:
                    return self.add1
                elif not self.add2.Busy:
                    return self.add2
            elif type == 'Mem':
                if not self.load0.Busy:
                    return self.load0
                elif not self.load1.Busy:
                    return self.load1
            elif type == 'Mul':                
                if not self.mult0.Busy:
                    return self.mult0
                elif not self.mult1.Busy:
                    return self.mult1
        else:
            raise Exception("No unit available: " + type)

    def is_load_available(self):
        return ((not self.load0.Busy) or (not self.load1.Busy))

    def is_add_available(self):
        return ((not self.add0.Busy) or (not self.add1.Busy) or (not self.add2.Busy))

    def is_mul_available(self):
        return ((not self.mult0.Busy) or (not self.mult1.Busy))

