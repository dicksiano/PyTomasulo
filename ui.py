import sys
sys.path.append('../presenter/')

import presenter

# PyQt5 dependencies
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Algoritmo de Tomasulo - Não especulativo'
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 800
        self.initUI()      
        self.presenter = presenter.Presenter()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createReservationStatusTable()
        self.createInstructionStatusTable()
        self.createRegisterStatusTable()
        self.createButton()

        # Add box layout, add tables to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.ReservationStatusTable)
        self.layout.addWidget(self.InstructionStatusTable)  
        self.layout.addWidget(self.RegisterStatusTable)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout) 
 
        # Show widget
        self.show()

    def createButton(self):
        self.button = QPushButton('Play', self)
        self.button.setToolTip('Next step of the algorithm execution')
        self.button.move(200,70) 
        self.button.clicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        self.presenter.update()
        [inst_info,reserv_info,reg_info]  = self.presenter.get_status()
        self.updateInstructionStatusTable(inst_info)
        self.updateReservationStatusTable(reserv_info)
        self.updateRegisterStatusTable(reg_info)

    def updateRegisterStatusTable(self, reg_info):
        for i in range(0,32):
            self.RegisterStatusTable.setItem(0, i + 1, QTableWidgetItem(str(reg_info[i])))

    def updateInstructionStatusTable(self, inst_info):
        for i in range(0, len(inst_info)):
            self.InstructionStatusTable.setItem(i, 0, QTableWidgetItem(str(inst_info[i][0])))
            if inst_info[i][1]:
                self.InstructionStatusTable.setItem(i, 1, QTableWidgetItem('X'))
            if inst_info[i][2]:
                self.InstructionStatusTable.setItem(i, 2, QTableWidgetItem('X'))
            if inst_info[i][3]:
                self.InstructionStatusTable.setItem(i, 3, QTableWidgetItem('X'))
            if inst_info[i][4]:
                self.InstructionStatusTable.setItem(i, 4, QTableWidgetItem('X'))

    def updateReservationStatusTable(self, reserv_info):
        for i in range(0, len(reserv_info)):
            for j in range(1, 8):
                if reserv_info[i][j] == 'none':
                    self.ReservationStatusTable.setItem(i, j, QTableWidgetItem(''))
                else:
                    self.ReservationStatusTable.setItem(i, j, QTableWidgetItem( str(reserv_info[i][j]) ))
 
    def createReservationStatusTable(self):
       # Create table
        self.ReservationStatusTable = QTableWidget()
        self.ReservationStatusTable.setRowCount(7)
        self.ReservationStatusTable.setColumnCount(8)

        self.ReservationStatusTable.setFixedSize(820,235)

        # Set headings
        self.ReservationStatusTable.setHorizontalHeaderLabels(["Name", "Busy", "Op", "Vj", "Vk", "Qj", "Qk", "A"])

        # Set execution unit names
        self.ReservationStatusTable.setItem(0,0, QTableWidgetItem("add0"))
        self.ReservationStatusTable.setItem(1,0, QTableWidgetItem("add1"))
        self.ReservationStatusTable.setItem(2,0, QTableWidgetItem("load0"))
        self.ReservationStatusTable.setItem(3,0, QTableWidgetItem("load1"))
        self.ReservationStatusTable.setItem(4,0, QTableWidgetItem("load2"))
        self.ReservationStatusTable.setItem(5,0, QTableWidgetItem("mult0"))
        self.ReservationStatusTable.setItem(6,0, QTableWidgetItem("mult1"))

        # Set position
        self.ReservationStatusTable.move(0,0)
 
    def createInstructionStatusTable(self):
       # Create table
        self.InstructionStatusTable = QTableWidget()
        self.InstructionStatusTable.setRowCount(300)
        self.InstructionStatusTable.setColumnCount(5)

        # Set headings
        self.InstructionStatusTable.setHorizontalHeaderLabels(["Op", "Write", "Execute", "Write", "Finalized"])

        # Set position
        self.InstructionStatusTable.move(310,0) 

    def createRegisterStatusTable(self):
       # Create table
        self.RegisterStatusTable = QTableWidget()
        self.RegisterStatusTable.setRowCount(1)
        self.RegisterStatusTable.setColumnCount(33)

        # Set headings
        self.RegisterStatusTable.setHorizontalHeaderLabels([
                            "Register", "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", 
                            "R10", "R11", "R12", "R13", "R14", "R15", "R16", "R17", "R18", "R19", 
                            "R20", "R21", "R22", "R23", "R24", "R25", "R26", "R27", "R28", "R29", 
                            "R30", "R31"])
        self.RegisterStatusTable.setItem(0,0, QTableWidgetItem("Qi"))

        # Set position
        self.RegisterStatusTable.move(200,0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())