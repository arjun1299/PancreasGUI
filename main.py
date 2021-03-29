import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer,QThreadPool,QThread
import serial
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon


from bleOperations import *
from logicModule import *
from multithread import *
from loggingModule import *
from PyQt5.QtTest import QTest
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
    """This is the main window's calss

    :param QtWidgets: Inherits Qwidgets
    :type QtWidgets: Qwidgets
    :param Ui_MainWindow: QMainWindow, obtained from the main GUI generated 
    :type Ui_MainWindow: QmainWindow
    :param connectTab: Parent class which deals with all the functions of connection associated with the connection Tab
    :type connectTab: Connect tab widget
    :param primingTab: Parent class which deals with all the functions of connection associated with the Priming Tab
    :type primingTab: [type]
    :param commandTab: Parent class which deals with all the functions of connection associated with the commend  Tab(Disabled)
    :type commandTab: [type]
    :param recurringTab: Parent class which deals with all the functions of connection associated with the recurring(dosages/deliveries) Tab
    :type recurringTab: [type]
    :param bolusTestingTab: Parent class which deals with all the functions of connection associated with the bolus activities
    :type bolusTestingTab: [type]
    """
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
        self.stopAllBtn.clicked.connect(self.stopAll)
        
        self.disconnectBtn =self.ui.DisconnectBtn

        self.disconnectBtn.clicked.connect(self.discon)

        self.timeDisplayLbl=self.ui.timeDisplayLbl
        self.timeUpdater=QTimer()
        self.timeUpdater.setInterval
        self.timeUpdater.timeout.connect(self.updateDateTime)
        self.updateDateTime()
        self.timeUpdater.start(900)
        

        #variables
        self.primingRotations=0
        #self.rotations=0
        self.actuationLength=0
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
        self.logger.loggerError.connect(self.loggerError)
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
        self.logic.insulonComplete.connect(self.resetHandler)
        self.logic.updateActuationLength.connect(self.updateActuationLength)
        self.logic.actuationLimitReached.connect(self.actuationLimitReached)
        self.logic.stopActuation.connect(self.stopActuation)
        self.logic.sendHB.connect(self.sender.sendHB)
        self.logic.sendIN.connect(self.sender.sendIN)
        self.logic.hbStop.connect(self.heartBeatChecker.hbStop)
        self.logic.sendDC.connect(self.sender.sendDC)
        self.logic.sendPC.connect(self.sender.sendPC)
        self.logic.sendUN.connect(self.sender.sendUN)
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


        self.ui.tabWidget.setTabEnabled(1,False)
        self.ui.tabWidget.setTabEnabled(2,False)
        self.ui.tabWidget.setTabEnabled(3,False)
        self.ui.tabWidget.setTabEnabled(4,False)
        self.ui.tabWidget.setTabEnabled(5,False)

        self.updateStatus()

    def loggerError(self):
        """Logger error is triggered if the logging module is not able to start 
        """
        self.showError("Logger Unable to start!")

    def stopAll(self):
        """Stop all is a layer on top of stopActuation, if OK is clicked then stop actuaion is executed and logged
        """
        if self.showDialog("Stop Actuation?")==QMessageBox.Ok:
            self.logic.pq.put((0,"STOP"))
            Logger.q.put(("WARNING","Stopping Actuation"))

    def updateDateTime(self):
        """Date and time maintainance on the main screen done here
        """
        timeStamp=datetime.datetime.now()
        timeStamp = timeStamp.strftime("Date: %d-%m-%Y\nTime: %H:%M:%S")
        self.timeDisplayLbl.setText(timeStamp)

    def stopActuation(self):
        """Sets all flags required to stop and stops all actuations. Priming or delivery all actuations are stopped
        """
        #deselect basal and bolus buttons
        self.buttonGroup.setExclusive(False)
        self.basalBtn.setChecked(False)
        self.bolusBtn.setChecked(False)
        self.buttonGroup.setExclusive(True)

        self.basalTimer.quit()
        self.bolusTimer.quit()
        self.stopPriming=True
        self.logic.allowActuation=False
        self.basalResume=False
        self.ongoingDeliveryFlag=False
        self.deliveryType=None
        self.heartBeatChecker.heartBeatSenderTimer.start()

    def resetActuation(self):
        """
        Stops actuation, gives an option for reversal and resets all values. This is to be typically used at the end of the actuation once the max length is reached and the reservoir is empty
        """
        
        if self.showDialog("Do you want to reset?\nWARNING: Reset Stop any ongoing deliveries, ensure that the actuator has been reset to the start position")==QMessageBox.Ok:
            num, ok = QInputDialog.getText(self, 'Number of reverse rotations', 'Number:')
            #self.logic.pq.put((1,"SPC"))
            self.stopActuation()

            if num.isnumeric():
                num=int(num)
            num=int(num)
            print("NUMBER OF ROTATIONS:"+str(num))
            
            for i in range(num):
                    self.logic.pq.put((1,"SUN"))
                    QTest.qWait(3000)

            
            self.init_primingTab()
            self.stopPriming=False
            self.logic.allowActuation=True
            self.actuationLength=0
            self.countTxt.setText(str(0))
            self.updateStatus()
            self.primingRotations=0
        
                
    def finished(self,args):
        """Once a thread is complete it can be linked to this function in order to know which function terminated

        :param args: String with process name
        :type args: string
        """
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
        """The status bar on the right side of the GUI is updated, both status bar and the delivery bar is updated in this function
        """
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
        self.statusTxt.appendPlainText("Actuation Length:"+str(self.actuationLength)+"mm")
        self.statusTxt.appendPlainText("Ongoing:"+ self.ongoing)
    
        # self.statusTxt.appendPlainText("Rotations: " + str(self.rotations))
        # self.statusTxt.appendPlainText("Previous dose: "+ self.prevTime)
        # self.statusTxt.appendPlainText("Next dose: "+ self.nextTime)
        # self.statusTxt.appendPlainText("Basal: "+ str(self.basalCnt))
        # self.statusTxt.appendPlainText("Bolus: "+ str(self.bolusCnt))

        if self.deliveryType!=None:
            self.doseStatusTxt.appendPlainText(self.deliveryType)
            if self.deliveryType=="Basal":
                self.doseStatusTxt.insertPlainText(", "+str(self.basalRate)+ " IU/hr")
            else:
                self.doseStatusTxt.insertPlainText(", "+ "{}ms , {}IU ".format(self.timeBetweenPulses,self.deliveryAmount))
        else:
            self.doseStatusTxt.appendPlainText("No delivery")
        #last delivery
        #future
        
    
    def showDialog(self,cmd):
        """
        Show a dialogue

        :param cmd: Text to be displayed in the dialogue box
        :type cmd: String
        :return: Action button which is pressed
        :rtype: QMessageBox standard buttons
        """
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(cmd)
        msgBox.setWindowTitle("Message")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        #msgBox.buttonClicked.connect(msgButtonClick)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')
        return returnValue

    def showWarning(self,cmd):
        """
        Show a warning message box

        :param cmd: Text to be displayed in the dialogue box
        :type cmd: String
        :return: Action button which is pressed
        :rtype: QMessageBox standard buttons
        """
        
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
        """
        Show a stop message box

        :param cmd: Text to be displayed in the dialogue box
        :type cmd: String
        :return: Action button which is pressed
        :rtype: QMessageBox standard buttons
        
        """
        #do one rotation
        if self.showDialog("Stop") == QMessageBox.Ok:
            self.deliveryType="None"
            self.basalBtn.checkStateSet(False)
            self.bolusBtn.checkStateSet(False)
            self.updateStatus()

    def discon(self):
        """
        Disconnect button links to this function, stops timers and disconects from GUI
        """
        
        if self.showDialog("Disconnect device?")== QMessageBox.Ok:
            self.bleConnectionStatus="Disconnected"
            self.ui.tabWidget.setCurrentIndex(0)
            self.stopActuation()
            self.uart_connection.disconnect()
            self.uart_service=False
            self.heartBeatChecker.heartBeatSenderTimer.stop()
            self.heartBeatChecker.heartBeatRecieverTimer.stop()
            self.updateStatus()
    
    """def closeEvent(self,event):
        Make sure all threads stop

        :param event: The close event which is raised, this is used
        :type event: 
        
        Logger.q.put(("INSTRUCTION","Stop"))
        SerialListner.SerialListnerEnable=False
        Parser.q.put("Stop")
        Logic.pq.put((1,"Stop"))
        event.accept() # let the window close

        self.logger.quit()
        self.serialListner.quit()
        self.parser.quit()
        self.logic.quit()
        event.accept()"""
        
    def updateActuationLength(self):
        """All insulon actuations will lead to this function and update the distance
        """
        #True is gear side
        #False is ratchet

        if self.checkActuationLimit():
            if(self.clutch==True):
                self.actuationLength+=0.36
            elif(self.clutch==False):
                self.actuationLength+=4.5*pow(10,-6)

        else:
            self.logic.allowActuation=False
            self.actuationLimitReached()
            self.stopActuation()
        
        self.updateStatus()

    def checkActuationLimit(self):
        """Checks actuation limit

        :return: Returns True-> allow actuation, limit not reached
        :rtype: Bool
        """
        if self.actuationLength < 27.0:
            return True
        return False
    def actuationLimitReached(self):
        self.showError("Actuation Limit reached")
        Logger.q.put(("ERROR","Actuation limit reached!"))
    def ratchetSlipOccoured(self):
        self.showError("Ratchet slip occoured")
        Logger.q.put(("ERROR","Ratchet slip occoured!"))


#app = QtWidgets.QApplication(sys.argv)
#window = MainWindow()
#window.show()
#app.aboutToQuit.connect(window.closeEvent)
#sys.exit(app.exec())