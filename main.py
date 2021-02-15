import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer,QThreadPool,QThread
import serial
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from bleOperations import *
from logicModule import *
from multithread import *

from basicui import Ui_MainWindow
import serial.tools.list_ports
from datetime import datetime as dt
from _connectTab import connectTab
from _primingTab import primingTab
from _commandTab import commandTab
from _recurringTab import recurringTab
from multithread import Worker,WorkerSignals

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow,connectTab,primingTab,commandTab,recurringTab):
    def __init__(self, *args, obj=None, **kwargs):
        
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        #status area
        self.statusTxt=self.ui.statusTxt
        self.doseStatusTxt= self.ui.doseStatusTxt
        self.connectionStatusLbl=self.ui.connectionStatusLbl
        
        self.stopAllBtn=self.ui.stopAllBtn
        self.stopAllBtn.clicked.connect(self.stop)
        
        self.disconnectBtn =self.ui.DisconnectBtn

        self.disconnectBtn.clicked.connect(self.discon)

        #variables
        self.primingRotations=0
        self.rotations=0
        self.ongoing= self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        self.basalCnt=0
        self.bolusCnt=0
        self.deliveryType="None"
        self.prevTime="HH:MM:SS"
        self.nextTime="HH:MM:SS"
        self.dose=0
        self.device=""
        self.bleConnectionStatus="Disconnected"

        self.targetAddress="f9:9b:81:05:de:e7"

        #False means rachet side
        #True is gear side
        self.clutch= False
        
        #initialize threading
        self.threadpool=QThreadPool()
        

        self.port=""
        
        self.init_connectTab()

        self.init_primingTab()
        
        self.init_commandTab()

        self.init_recurringTab()


        
        self.updateStatus()

        """
        Start serial listener and connect it to parser queue

        """
        
        self.serialListner =SerialListner()
        self.serialListner.dataArrival.connect(self.addToParserQueue)
        self.serialListner.start()
        
        
        """
        Section to start parser
        """
        self.parser=Parser()
        self.parser.addToLogicQueue.connect(self.addToLogicQueue)
        self.parser.start()       

        """
        Start sender 
        """ 
        self.sender=Sender()
        self.sender.sendData.connect(self.sendData)
        self.sender.start()   

        """Initialize connection checker which checks heartbeat
        """

        self.connectionChecker=connectionChecker()
        self.connectionChecker.sendHeartBeat.connect(self.sender.sendHB)
        self.connectionChecker.timeoutSignal.connect(self.heartBeatTimeout)

        """
        Section to Logic
        """
        self.logic=Logic()
        ###Connect all logic signals
        self.logic.hbTimerReset.connect(self.connectionChecker.hbTimerReset)
        self.logic.start()   

        self.connectedSignal.connect(self.isConnectedBLEHandle)

    
    

    def isConnectedBLEHandle(self):
        """
        Initialize thread to check if ble is connected
        """
        print("Starting hb")

        worker=Worker(self.isConnectedBLE)
        worker.signals.finished.connect(self.finish)
        self.connectionChecker.heartBeatSenderTimer.start(500)
        self.connectionChecker.heartBeatRecieverTimer.start(5000)
        self.connectionChecker.heartBeatRecieverTimer.timeout.connect(self.heartBeatTimeout)
        self.threadpool.start(worker)


                
    def finished(self):
        print("Done!!!!!!!!!!!!!")

    def addToLogicQueue(self,args):
        """Adds argument to logic queue for processing
        :param args: A string which is used by the logic module if-else ladder
        :type args: String
        """
        self.logic.pq.put(args)
        print("Added to Logic queue")


    def heartBeatTimeout(self):
        """
        Timeout function if hearbeat is not recieved in time
        """

        self.connectionChecker.heartBeatRecieverTimer.stop()
        self.connectionChecker.heartBeatSenderTimer.stop()
        self.uart_service=False

        self.showError("Heart beat missing")
        self.init_connectTab()
        self.showError("Device disconnected")
        self.bleConnectionStatus="Disconnected"
        self.updateStatus()
        
        self.ui.tabWidget.setCurrentIndex(0)
        self.disconnectBtn.setEnabled(False)
        self.uart_connection.disconnect()

    def sendData(self,data):
        """Function to send data via the Bluetooth adapter to the BLE module on the device

        :param data: A stromg which needs to be sent over ble
        :type data: String
        """
        if self.uart_service:
            self.uart_service.write(data.encode("utf-8"))
            print("Sent: "+data)





    def isConnectedBLE(self):
        """
        Checks if the BLE module is still connected to the device
        """
        
        while 1:
            if self.uart_service:
                if self.uart_connection.connected:
                    pass
                else:
                    self.uart_service=False
            time.sleep(0.1)

    def addToParserQueue(self):
        """
        This function is used by the listener to keep adding data into the parser queue 
        """
        if(self.uart_service):
            while(self.uart_service.in_waiting):# if an if condition is used partially read charachters appear
                raw_serial=self.uart_service.readline()
                if raw_serial:
                    self.parser.q.put(raw_serial)
                    print("Added to parser queue")
        else:
            print("No UART connection, cannot add to parser Queue")

    def updateStatus(self):
        self.statusTxt.clear()
        self.doseStatusTxt.clear()

        #self.statusTxt.appendPlainText("Reciever Status:" +  ("Connected" if self.isConnectedReciever() else "Disconnected" ))
        self.statusTxt.appendPlainText("BLE Status:" + self.bleConnectionStatus )
        if self.bleConnectionStatus=="Connected":
            self.connectionStatusLbl.setStyleSheet("background-color: rgb(41, 239, 41)")
        elif self.bleConnectionStatus=="Scanning":
            self.connectionStatusLbl.setStyleSheet("background-color: rgb(252, 233, 79)")
        else:
            self.connectionStatusLbl.setStyleSheet("background-color: rgb(239, 41, 41)")
        self.statusTxt.appendPlainText("Clutch: "+ ("Gear" if self.clutch else "Ratchet"))

        self.statusTxt.appendPlainText("Ongoing:"+ self.ongoing)
    
        # self.statusTxt.appendPlainText("Rotations: " + str(self.rotations))
        # self.statusTxt.appendPlainText("Previous dose: "+ self.prevTime)
        # self.statusTxt.appendPlainText("Next dose: "+ self.nextTime)
        # self.statusTxt.appendPlainText("Basal: "+ str(self.basalCnt))
        # self.statusTxt.appendPlainText("Bolus: "+ str(self.bolusCnt))

        
        
        self.doseStatusTxt.appendPlainText(self.deliveryType)
        if self.deliveryType!="None":
            #self.doseStatusTxt.appendPlainText(str(self.dose))
            self.doseStatusTxt.insertPlainText(", "+str(self.dose)+ (" IU/hr" if self.deliveryType=="Basal" else "IU"))
        #last delivery
        #future
        
    
    def showDialog(self,cmd):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Send command "+cmd+" ?")
        msgBox.setWindowTitle("Message")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        #msgBox.buttonClicked.connect(msgButtonClick) 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')
        return returnValue
        self.basalBtn.checkStateSet(True)

    def showWarning(self,cmd):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(cmd)
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(QMessageBox.Ok)
        #msgBox.buttonClicked.connect(msgButtonClick) 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')
        return returnValue
        self.basalBtn.checkStateSet(True)
    
    def showError(self,cmd):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText(cmd)
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(QMessageBox.Ok)
        #msgBox.buttonClicked.connect(msgButtonClick) 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')
        return returnValue
        self.basalBtn.checkStateSet(True)
    
    def stop(self):
        #do one rotation
        if self.showDialog("Stop") == QMessageBox.Ok:
            self.deliveryType="None"
            self.basalBtn.checkStateSet(False)
            self.bolusBtn.checkStateSet(False)
            self.updateStatus()

    def discon(self):
        
        if self.showDialog("Disconnect")== QMessageBox.Ok:
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.tabWidget.currentIndex
            self.uart_connection.disconnect()

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec())