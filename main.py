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
from loggingModule import *

from basicui import Ui_MainWindow
import serial.tools.list_ports
from datetime import datetime as dt
from _connectTab import connectTab
from _primingTab import primingTab
from _commandTab import commandTab
from _recurringTab import recurringTab
from _bolusTesting import bolusTestingTab
from multithread import Worker,WorkerSignals

import sys
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow,connectTab,primingTab,commandTab,recurringTab,bolusTestingTab):
    def __init__(self, *args, obj=None, **kwargs):
        sys.setswitchinterval(0.0000001)

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

        """
        Start logging module
        """

        self.logger= Logger()
        self.logger.start()
        #self.sender.finished.connect(lambda v: self.finished("Logger"))

        """
        Start serial listener and connect it to parser queue

        """
        
        self.serialListner =SerialListner()
        self.serialListner.dataArrival.connect(self.addToParserQueue)
        #self.sender.finished.connect(lambda v: self.finished("Listner"))
        self.serialListner.start()
        
        
        """
        Section to start parser
        """
        self.parser=Parser()
        self.parser.addToLogicQueue.connect(self.addToLogicQueue)
        #self.sender.finished.connect(lambda v: self.finished("Parser"))
        self.parser.start()       

        self.logic=Logic()
        """
        Start sender 
        """ 
        self.sender=Sender()
        self.sender.sendData.connect(self.sendData)
        #self.sender.finished.connect(lambda v: self.finished("Sender"))
        self.sender.heartBeatSent.connect(self.logic.heartBeatSent)
        self.sender.insulonSent.connect(self.logic.insulonSent)
        self.sender.start()
        

        self.heartBeatChecker=heartBeatChecker()
        """
        Section to Logic
        """
        
        ###Connect all logic signals
        self.logic.hbSenderTimerReset.connect(self.heartBeatChecker.hbSenderTimerReset)
        self.logic.hbRecieverTimerReset.connect(self.heartBeatChecker.hbRecieverTimerReset)
        self.logic.insulonComplete.connect(self.resetBolusTimer)
        self.logic.sendHB.connect(self.sender.sendHB)
        self.logic.sendIN.connect(self.sender.sendIN)
        self.logic.hbStop.connect(self.heartBeatChecker.hbStop)
        self.logic.sendDC.connect(self.sender.sendDC)
        self.logic.sendPC.connect(self.sender.sendPC)
        self.logic.start()

        self.connectedSignal.connect(self.isConnectedBLEHandle)
        

        """Initialize connection checker which checks heartbeat
        """
        self.heartBeatChecker.sendHeartBeat.connect(self.logic.addHBLogic)
        self.heartBeatChecker.timeoutSignal.connect(self.heartBeatTimeout)


        """
        Inititialize all the required tabs
        """

        self.port=""
        
        self.init_connectTab()

        self.init_primingTab()

        self.init_commandTab()

        self.init_recurringTab()

        self.init_bolusTestingTab() 


        
        self.updateStatus()


                
    def finished(self,args):
        print(args+"Thread complete")
        Logger.q.put(("WARNING",args+"Thread complete"))

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

        self.heartBeatChecker.heartBeatRecieverTimer.stop()
        self.heartBeatChecker.heartBeatSenderTimer.stop()
        self.uart_service=False
        Logger.q.put(("ERROR","Heartbeat Timeout!!"))
        self.showError("Heart beat missing")
        
        while Logger.q.empty()==False or self.parser.q.empty()==False or self.sender.q.empty()==False or self.logic.pq.empty()==False: 
            time.sleep(0.0005)
    
        self.showError("Device disconnected")
        self.bleConnectionStatus="Disconnected"
        self.init_connectTab()
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
            Logger.q.put(("INFO","Sent"+data))
            print("Sent: "+data)






    def addToParserQueue(self):
        """
        This function is used by the listener to keep adding data into the parser queue 
        """
        if(self.uart_service):
            while(self.uart_service.in_waiting):# if an if condition is used partially read charachters appear
                Logger.q.put(("INFO","Data in buffer"))
                raw_serial=self.uart_service.readline()
                if raw_serial:
                    self.parser.q.put(raw_serial)
                    Logger.q.put(("INFO","Data added to parser queue"))
                    print("Added to parser queue")
        """else:
            print("No UART connection, cannot add to parser Queue"
        """

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
    
    def closeEvent(self,event):
        """Make sure all threads stop

        :param event: The close event which is raised, this is used
        :type event: 
        """
        """Logger.q.put(("INSTRUCTION","Stop"))
        SerialListner.SerialListnerEnable=False
        Parser.q.put("Stop")
        Logic.pq.put((1,"Stop"))
        event.accept() # let the window close"""

        self.logger.quit()
        self.serialListner.quit()
        self.parser.quit()
        self.logic.quit()
        event.accept()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())