import sys
from PyQt5 import QtWidgets, uic
import serial
from basicui import Ui_MainWindow
import serial.tools.list_ports
from datetime import datetime as dt
import os


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.port=""
        
        self.statusTxt= self.ui.statusTxt

        self.init_connectTab()

        self.init_commandTab()

        self.init_recurringTab()

        self.init_primingTab()
        
        self.rotations=0
        self.ongoing= self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        
        self.updateStatus()

    def updateStatus(self):
        self.statusTxt.clear()
        self.statusTxt.appendPlainText("Reciever Status:" +  ("Connected" if self.isConnectedReciever() else "Disconnected" ))
        self.statusTxt.appendPlainText("BLE Status:" + ("Connected" if self.isConnectedBLE() else "Disconnected") )
        self.statusTxt.appendPlainText("Rotations: " + str(self.rotations))
        self.statusTxt.appendPlainText("Ongoing:"+ self.ongoing)

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
        self.connectButton.setEnabled(False)
        self.connectButton.clicked.connect(self.connectPort)
        

    def isConnectedBLE(self):
        #check for heartbeat here
        pass

        return 0

    def isConnectedReciever(self):
        #checks if bluetooth reciever is connected
        if(os.system("hcitool scan")== 256):
            return 0
        return 1


    def chk(self):
        #enable tabs
        #self.ui.tabWidget.setTabEnabled(1,self.isConnectedBLE())
        #self.ui.tabWidget.setTabEnabled(2,self.isConnectedBLE())
        pass


    def connectPort(self):
        if(self.dropdown.currentText()):
            self.port=self.dropdown.currentText()
            
            """
            #add logic to pair with BLE
            """

            print("Connected to:"+self.dropdown.currentText())
    
    def scanPort(self):
        
        print("Scanning...")
        
        self.ongoing="Scanning"
        self.updateStatus()
        
        
        if(self.isConnectedReciever):
            self.updateStatus()
            return 0
        
        cmd=os.popen("hcitool scan")
        
        comlist = cmd.read()
        
        comlist = comlist.split('\n')
        
        #the last element is empty 
        comlist.pop()

        connected = []
        self.dropdown.clear()
        for element in comlist:
            connected.append(element.device)
            self.dropdown.addItem(element.device)
        
        self.connectButton.setEnabled(True)

    """
    Tab-2

    """

    def init_primingTab(self):
        #start prime
        self.startPrime=self.ui.startPrime
        self.startPrime.clicked.connect(self.enablePriming)
        #rotate
        self.rotateBtn=self.ui.rotateBtn
        self.rotateBtn.setEnabled(False)

        #stop
        self.stopBtn=self.ui.stopBtn
        self.stopBtn.setEnabled(False)

    def enablePriming(self):
        self.rotateBtn.setEnabled(True)
        self.stopBtn.setEnabled(True)
        self.updateStatus()

    def rotate(self):
        #do one rotation
        pass


    def stop(self):
        #do one rotation
        pass
    
    """
    Tab-3

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
    Tab-4
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
