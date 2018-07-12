import sys
sys.path.append('../presenter/')

import presenter

# PyQt5 dependencies
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QFileDialog, QHeaderView, QLabel
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot, Qt
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Algoritmo de Tomasulo - Não especulativo'
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 800
        self.count = 0

        self.initUI()      
        fileName = self.openFileNameDialog()
        self.presenter = presenter.Presenter(fileName)
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createReservationStatusTable()
        self.createInstructionStatusTable()
        self.createFirstRegisterStatusTable()
        self.createSecondRegisterStatusTable()
        self.createPlayButton()

        # Add box layout, add tables to box layout and add box layout to widget
        self.layout = QVBoxLayout()

        # Reservation Station
        self.l1 = QLabel("Reservation Station")
        self.l1.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.l1)
        self.layout.addStretch()
        self.layout.addWidget(self.ReservationStatusTable)

        self.l2 = QLabel("                                                                               Instructions")
        self.layout.addWidget(self.l2)
        self.layout.addStretch()
        self.layout.addWidget(self.InstructionStatusTable)
        
        self.l3 = QLabel("Registers")
        self.l3.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.l3)
        self.layout.addStretch()  
        self.layout.addWidget(self.FirstRegisterStatusTable)
        self.layout.addWidget(self.SecondRegisterStatusTable)
        self.layout.addWidget(self.playButton)
        self.setLayout(self.layout) 
        # Show widget
        self.show()

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Escolha o seu arquivo de entrada.", "","Txt Files (*.txt)", options=options)
        if fileName:
            return fileName

    def createPlayButton(self):
        self.playButton = QPushButton('Play', self)
        self.playButton.setToolTip('Next step of the algorithm execution')
        self.playButton.move(200,70) 
        icon = QIcon("play.png")
        self.playButton.setIcon(icon)
        self.playButton.clicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        self.presenter.update()
        [cycle, issued_inst, inst_info,reserv_info,reg_info]  = self.presenter.get_status()
        self.l1.setText("Reservation Station - Cycle " + str(cycle) + " - Issued " + str(issued_inst))
        self.updateInstructionStatusTable(inst_info)
        self.updateReservationStatusTable(reserv_info)
        self.updateFirstRegisterStatusTable(reg_info)
        self.updateSecondRegisterStatusTable(reg_info)

    def updateFirstRegisterStatusTable(self, reg_info):
        for i in range(0,16):
            item = QTableWidgetItem(str(reg_info[i]))
            item.setTextAlignment(Qt.AlignCenter)
            self.FirstRegisterStatusTable.setItem(0, i + 1, item)

            if not str(reg_info[i]).isdigit():
                self.FirstRegisterStatusTable.item(0, i + 1).setBackground(QColor(250,0,0))

    def updateSecondRegisterStatusTable(self, reg_info):
        for i in range(0,16):
            item = QTableWidgetItem(str(reg_info[i+15]))
            item.setTextAlignment(Qt.AlignCenter)
            self.SecondRegisterStatusTable.setItem(0, i + 1 , item)

            if not str(reg_info[i + 15]).isdigit():
                self.SecondRegisterStatusTable.item(0, i + 1).setBackground(QColor(250,0,0))

    def updateInstructionStatusTable(self, info):
        [program_counter, inst_info] = [info[0], info[1]]
        for i in range(0, len(inst_info)):
            self.InstructionStatusTable.setItem(i, 0, QTableWidgetItem(str(inst_info[i][0])))

            #PC
            if i == program_counter:
                self.InstructionStatusTable.item(i, 0).setBackground(QColor(0,0,250))
            else:
                self.InstructionStatusTable.item(i, 0).setBackground(QColor(255,255,255))

            if inst_info[i][1]:
                self.InstructionStatusTable.setItem(i, 1, QTableWidgetItem(' '))
                self.InstructionStatusTable.item(i, 1).setBackground(QColor(0,150,0))
            else:
                self.InstructionStatusTable.setItem(i, 1, QTableWidgetItem(' '))
                self.InstructionStatusTable.item(i, 1).setBackground(QColor(255,255,255))

            if inst_info[i][2]:
                self.InstructionStatusTable.setItem(i, 2, QTableWidgetItem(' '))
                self.InstructionStatusTable.item(i, 2).setBackground(QColor(0,150,0))
            else:
                self.InstructionStatusTable.setItem(i, 2, QTableWidgetItem(' '))
                self.InstructionStatusTable.item(i, 2).setBackground(QColor(255,255,255))

            if inst_info[i][3]:
                self.InstructionStatusTable.setItem(i, 3, QTableWidgetItem(' '))
                self.InstructionStatusTable.item(i, 3).setBackground(QColor(0,150,0))
            else:
                self.InstructionStatusTable.setItem(i, 3, QTableWidgetItem(' '))
                self.InstructionStatusTable.item(i, 3).setBackground(QColor(255,255,255))

            if inst_info[i][4]:
                self.InstructionStatusTable.setItem(i, 4, QTableWidgetItem(' '))
                self.InstructionStatusTable.item(i, 4).setBackground(QColor(0,150,0))
            else:
                self.InstructionStatusTable.setItem(i, 4, QTableWidgetItem(' '))
                self.InstructionStatusTable.item(i, 4).setBackground(QColor(255,255,255))

    def updateReservationStatusTable(self, reserv_info):
        for i in range(0, len(reserv_info)):
            for j in range(1, 8):
                if reserv_info[i][j] == 'none':
                    self.ReservationStatusTable.setItem(i, j, QTableWidgetItem(''))
                else:
                    item = QTableWidgetItem(str(reserv_info[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ReservationStatusTable.setItem(i, j, item)
                    if j == 5 or j == 6:
                        self.ReservationStatusTable.item(i, j).setBackground(QColor(250,0,0))
 
    def createReservationStatusTable(self):
       # Create table
        self.ReservationStatusTable = QTableWidget()
        self.ReservationStatusTable.setRowCount(7)
        self.ReservationStatusTable.setColumnCount(8)

        self.ReservationStatusTable.setFixedSize(1200,235)

        # Set headings
        self.ReservationStatusTable.setHorizontalHeaderLabels(["Name", "Busy", "Op", "Vj", "Vk", "Qj", "Qk", "A"])

        # Set execution unit names
        item = QTableWidgetItem("load0")
        item.setTextAlignment(Qt.AlignCenter)
        self.ReservationStatusTable.setItem(0,0, item)
        self.ReservationStatusTable.item(0,0).setBackground(QColor(150,150,150))

        item = QTableWidgetItem("load1")
        item.setTextAlignment(Qt.AlignCenter)
        self.ReservationStatusTable.setItem(1,0, item)
        self.ReservationStatusTable.item(1,0).setBackground(QColor(150,150,150))

        item = QTableWidgetItem("add0")
        item.setTextAlignment(Qt.AlignCenter)
        self.ReservationStatusTable.setItem(2,0, item)
        self.ReservationStatusTable.item(2,0).setBackground(QColor(150,150,150))

        item = QTableWidgetItem("add1")
        item.setTextAlignment(Qt.AlignCenter)
        self.ReservationStatusTable.setItem(3,0, item)
        self.ReservationStatusTable.item(3,0).setBackground(QColor(150,150,150))

        item = QTableWidgetItem("add2")
        item.setTextAlignment(Qt.AlignCenter)
        self.ReservationStatusTable.setItem(4,0, item)
        self.ReservationStatusTable.item(4,0).setBackground(QColor(150,150,150))

        item = QTableWidgetItem("mult0")
        item.setTextAlignment(Qt.AlignCenter)
        self.ReservationStatusTable.setItem(5,0, item)
        self.ReservationStatusTable.item(5,0).setBackground(QColor(150,150,150))

        item = QTableWidgetItem("mult1")
        item.setTextAlignment(Qt.AlignCenter)
        self.ReservationStatusTable.setItem(6,0, item)
        self.ReservationStatusTable.item(6,0).setBackground(QColor(150,150,150))

        # Set position
        self.ReservationStatusTable.move(0,0)

        # Column width
        self.ReservationStatusTable.setColumnWidth(0,145)
        self.ReservationStatusTable.setColumnWidth(1,120)
        self.ReservationStatusTable.setColumnWidth(2,195)
        self.ReservationStatusTable.setColumnWidth(3,145)
        self.ReservationStatusTable.setColumnWidth(4,145)
        self.ReservationStatusTable.setColumnWidth(5,145)
        self.ReservationStatusTable.setColumnWidth(6,145)
        self.ReservationStatusTable.setColumnWidth(7,145)
 
    def createInstructionStatusTable(self):
       # Create table
        self.InstructionStatusTable = QTableWidget()
        self.InstructionStatusTable.setRowCount(300)
        self.InstructionStatusTable.setColumnCount(5)
        self.InstructionStatusTable.setFixedSize(627,235)

        self.InstructionStatusTable.setColumnWidth(0, 180)
        self.InstructionStatusTable.setColumnWidth(1, 100)
        self.InstructionStatusTable.setColumnWidth(2, 100)
        self.InstructionStatusTable.setColumnWidth(3, 100)
        self.InstructionStatusTable.setColumnWidth(4, 100)

        # Set headings
        self.InstructionStatusTable.setHorizontalHeaderLabels(["Op", "Issue", "Execute", "Write", "Finalized"])

        # Set position
        self.InstructionStatusTable.move(310,0) 

    def createFirstRegisterStatusTable(self):
       # Create table
        self.FirstRegisterStatusTable = QTableWidget()
        self.FirstRegisterStatusTable.setRowCount(1)
        self.FirstRegisterStatusTable.setColumnCount(17)
        self.FirstRegisterStatusTable.setFixedSize(1200,50)

        self.FirstRegisterStatusTable.setColumnWidth(0,81)
        for i in range(1,33):
            self.FirstRegisterStatusTable.setColumnWidth(i, 69)

        # Set headings
        self.FirstRegisterStatusTable.setHorizontalHeaderLabels([
                            "Register", "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", 
                            "R10", "R11", "R12", "R13", "R14", "R15"])
        item = QTableWidgetItem("Qi")
        item.setTextAlignment(Qt.AlignCenter)
        self.FirstRegisterStatusTable.setItem(0,0, item)

        # Set position
        self.FirstRegisterStatusTable.move(200,0)

    def createSecondRegisterStatusTable(self):
       # Create table
        self.SecondRegisterStatusTable = QTableWidget()
        self.SecondRegisterStatusTable.setRowCount(1)
        self.SecondRegisterStatusTable.setColumnCount(17)
        self.SecondRegisterStatusTable.setFixedSize(1200,50)

        self.SecondRegisterStatusTable.setColumnWidth(0,81)
        for i in range(1,33):
            self.SecondRegisterStatusTable.setColumnWidth(i, 69)

        # Set headings
        self.SecondRegisterStatusTable.setHorizontalHeaderLabels([
                            "Register", "R16", "R17", "R18", "R19", "R20", "R21", 
                            "R22", "R23", "R24", "R25", "R26", "R27", "R28", "R29", 
                            "R30", "R31"])
        item = QTableWidgetItem("Qi")
        item.setTextAlignment(Qt.AlignCenter)
        self.SecondRegisterStatusTable.setItem(0,0, item)

        # Set position
        self.SecondRegisterStatusTable.move(200,0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())