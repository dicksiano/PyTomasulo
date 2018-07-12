"""
	Class that represents a o model of the machine
	"""
class Memomy_Model:
    def __init__(self):
        self.memory = []
        for i in range(0, 4000):
            self.memory.append(i*0)
        
    def get(self, adress):
        return self.memory[int(adress)]

    def set(self, adress, value):
        self.memory[int(adress)] = value