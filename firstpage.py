from PyQt5 import QtCore, QtGui, QtWidgets
import visa
import time
import math
from RsInstrument.RsInstrument import RsInstrument
from secondpage import Ui_SecondWindow


class Ui_MainWindow(object):

    def Nextpage(self):
        self.pencere=QtWidgets.QMainWindow()
        self.ui=Ui_SecondWindow()
        self.ui.setupUi(self.pencere)
        self.pencere.show()
        MainWindow.close()


    def Check96270A(self):
        a = visa.ResourceManager()
        Fluke = a.get_instrument('GPIB0::18::INSTR')
        identity=Fluke.query('*IDN?')
        self.label.setText(identity)
        self.label.setStyleSheet("background-color:#07da63;")

    def CheckRohdeSchwarz(self):
        a=visa.ResourceManager()
        ResourceTupple = a.list_resources()
        ResorceStringList=[]
        instrumentname=''
        for i in ResourceTupple:
            ResorceStringList.append(i)
        for i in ResorceStringList:
            if i.startswith('USB'):
                instrumentname=i

        PowerSensor = a.get_instrument(instrumentname)
        identity=PowerSensor.query('*IDN?')
        self.label_2.setText(identity)
        self.label_2.setStyleSheet("background-color:#07da63;")


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(697, 445)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 100, 231, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setDefault(True)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 200, 231, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setDefault(True)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 100, 221, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAutoFillBackground(True)
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton.clicked.connect(self.Check96270A)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(400, 200, 221, 61))
        self.pushButton_2.clicked.connect(self.CheckRohdeSchwarz)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAutoFillBackground(True)
        self.label_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(550, 360, 71, 41))
        self.pushButton_3.clicked.connect(self.Nextpage)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setDefault(True)
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CalFactor"))
        self.pushButton.setText(_translate("MainWindow", "96270A \n Connection Check \n Set the GPIB to 18"))
        self.pushButton_2.setText(_translate("MainWindow", "NRP Power Sensor \n Connection Check"))
        self.pushButton_3.setText(_translate("MainWindow", "Next"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

