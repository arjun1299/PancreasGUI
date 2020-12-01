import sys
from PyQt5 import QtWidgets, uic
import serial
from basicui import Ui_MainWindow
import serial.tools.list_ports
from datetime import datetime as dt

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.port=""
        
        self.init_connectTab()

        self.init_commandTab()

        self.init_recurringTab()

    """
        Tab 1- connect tab
    """

    def init_connectTab(self):

        self.check=self.ui.checkBox
        self.chk()
        self.check.clicked.connect(self.chk)
        #dropdown
        self.dropdown=self.ui.comboBox
        #scan button
        self.scanButton=self.ui.scanButton
        self.scanButton.clicked.connect(self.scanPort)
        #connect button
        self.connectButton=self.ui.connectButton
        self.connectButton.clicked.connect(self.connectPort)
        

    def isConnected(self):
        if self.port=="":
            return False
        return True

    def chk(self):
        self.ui.tabWidget.setTabEnabled(1,self.isConnected())
        self.ui.tabWidget.setTabEnabled(2,self.isConnected())
    
    def connectPort(self):
        if(self.dropdown.currentText()):
            self.port=self.dropdown.currentText()
            self.chk()
            print("Connected to:"+self.dropdown.currentText())
    
    def scanPort(self):
        
        print("Scanning...")

        comlist = serial.tools.list_ports.comports()
        connected = []
        self.dropdown.clear()
        for element in comlist:
            connected.append(element.device)
            self.dropdown.addItem(element.device)

    """
    Tab-2
    """

    def init_commandTab(self):
        self.sendButton=self.ui.SendButton
        self.cmdTxt=self.ui.cmdTxt
        self.outTxt=self.ui.outTxt
        self.sendButton.clicked.connect(self.sendButtonClick)

    def sendButtonClick(self):
        self.sendCommand(self.cmdTxt.toPlainText())
        self.outTxt.appendPlainText(self.cmdTxt.toPlainText())
        
    def sendCommand(self,text):
        print("Sending:"+text)
        ser=serial.Serial(self.port)
        text=bytes(text,'utf-8')
        ser.write(text)
        ser.close()
        


    """
    Tab-3
    """

    def init_recurringTab(self):
        self.setButton=self.ui.SetButton
        self.reCmdTxt=self.ui.reCmdTxt
        self.reOutTxt=self.ui.reOut
        self.reTime=self.ui.reTime
        self.setButton.clicked.connect(self.reSendCommand)
        
    def reSendCommand(self):
        
        delay= float(self.reTime.toPlainText())
        print(delay)
        start=dt.now()
        while 1:
            end=dt.now()
            diff=(end-start).seconds+(end-start).microseconds*pow(10,-6)
            
            if(diff>=delay):
                self.sendCommand(self.reCmdTxt.toPlainText())
                self.reOutTxt.appendPlainText(self.reCmdTxt.toPlainText())
                start=dt.now()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()