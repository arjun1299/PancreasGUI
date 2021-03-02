from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer,QThreadPool,QThread

from basicui import Ui_MainWindow
from bleOperations import *
import time

class bolusTestingTab(object):
    def __init__(self):
        super().__init__()

    def init_bolusTestingTab(self):
        #start prime
        self.ongoingDeliveryFlag=False

        self.startPrimeBtn=self.ui.startPrimeBtn
        self.startPrimeBtn.clicked.connect(self.enablePriming)
        self.pulseDelayTxt= self.ui.pulseDelayTxt
        self.deliveryAmtTxt= self.ui.deliveryAmtTxt

        self.startBolusBtn=self.ui.startBolusBtn
        self.startBolusBtn.clicked.connect(self.startBolusDelivery)
        self.stopBolusBtn=self.ui.stopBolusBtn

        #self.bolusTimer=QTimer()
        #self.bolusTimer.timeout.connect(self.bolusDose)
        self.bolusTimer=timerThread()
        self.bolusTimer.timeoutSignal.connect(self.bolusDose)
        
        #self.bolusTimer.moveToThread(self.logic)
        
        self.completedDose=0
        self.timeBetweenPulses=0

        #Time duration  monitoring
        self.insulonStartTime=0
        self.insulonEndTime=0
        self.prevTime=0

        self.insulonCompleteFlag=False
    
    def startBolusDelivery(self):
        self.insulonCompleteFlag=True
        self.ongoingDeliveryFlag=True
        self.heartBeatChecker.heartBeatSenderTimer.stop()
        self.heartBeatChecker.heartBeatRecieverTimer.stop()
        
        """Steps:
        1. Send HB
        2. Recieve reply HB
        3. Send IN based on  heartbeat response
        """
        print("Starting Bolus Delivery")
        
        self.timeBetweenPulses=int(self.pulseDelayTxt.toPlainText())
        self.deliveryAmount=int(self.deliveryAmtTxt.toPlainText())
        Logger.q.put(("WARNING","Starting Bolus Delivery with duration {} for {}IU ".format(self.timeBetweenPulses,self.deliveryAmount)))
        self.showWarning("Start Bolus Delivery with duration {} for {}IU ?".format(self.timeBetweenPulses,self.deliveryAmount))
        self.completedDose=0
        #self.timeBetweenPulses=2000
        self.bolusTimer.setTimeout(self.timeBetweenPulses)
        self.bolusTimer.finished.connect(self.completedBolusRegime)
        self.bolusTimer.start()
        self.bolusTimer.setPriority(QThread.HighestPriority)

    
    def setInsulonCompleteFlag(self,status):
        self.insulonCompleteFlag= status

    def resetBolusTimer(self,encoderValue):
        
        """Resets the bolus timer if the delivery target has not been reached

        :param timeDelay: String, it has to be converted to an int before
        :type timeDelay: string
        """
        Logger.q.put(("INFO","Encoder value: {}".format(encoderValue)))
        if(self.ongoingDeliveryFlag==False):
            return

        if self.deliveryAmount>0:
                self.insulonCompleteFlag=True
                self.deliveryAmount-=1 #decrease by amount consumed in 1 rotation
                Logger.q.put(("WARNING","Resetting bolus delivery timer,{} remaining".format(self.deliveryAmount)))
                print("Reset Bolus timer")

                
                #self.bolusTimer.start()
                
                #This method uses delay given by the device
                #self.bolusTimer.start(abs(int(self.timeBetweenPulses-int(timeDelay))))
                print("Time Delay: ")
                self.insulonEndTime=current_milli_time()
                print(self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))
                #self.bolusTimer.start(self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))#self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))
                #self.bolusTimer.setTimeout(self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))#self.timeBetweenPulses)
                #self.bolusTimer.quit()
                
                timediff=(self.insulonEndTime-self.insulonStartTime)
                
                #constant time delay
                self.bolusTimer.setTimeout(self.timeBetweenPulses-timediff)
                self.bolusTimer.start()
            

                #self.deliveryAmount+=1


                """
                if(self.timeBetweenPulses-timediff>=0):
                    self.bolusTimer.setTimeout(self.timeBetweenPulses-timediff)
                    Logger.q.put(("INFO","Timeout:{}".format(self.timeBetweenPulses-timediff)))
                            
                self.bolusTimer.start()
                """
            
        else:
            #self.bolusTimer.stopTimer()
            self.bolusTimer.quit()
            Logger.q.put(("WARNING","Completed Bolus Delivery"))
            self.ongoingDeliveryFlag=False

    def stopBolusDelivery():
        self.showWarning("Stop Bolus Delivery?")
        Logger.q.put(("WARNING","Stopped Bolus Delivery"))
        self.bolusTimer.quit()
        #self.bolusTimer.stop()

    def bolusDose(self):
        #if the previous dose is complete only then send the next should start
        if self.insulonCompleteFlag==True:
            self.insulonStartTime=current_milli_time()
            print("Sent bolus dose",self.insulonStartTime)
            print("Time difference::::::",self.insulonStartTime-self.prevTime)
            Logger.q.put(("INFO","Time difference between deliveries ::::{}".format(self.insulonStartTime-self.prevTime)))
            #self.sender.q.put("IPIN\r")
            self.logic.pq.put((1,"INSHB"))
            #self.uart_service.write("IPIN\r".encode("utf-8"))
            self.prevTime=self.insulonStartTime
            self.insulonCompleteFlag=False
        else:
            Logger.q.put(("ERROR","Response too slow, Skipping delivery"))


        #Start timer
    def completedBolusRegime(self):
        self.heartBeatChecker.heartBeatSenderTimer.stop()
        self.heartBeatChecker.heartBeatRecieverTimer.stop()
        
        self.heartBeatChecker.heartBeatSenderTimer.start()
        
        
def current_milli_time():
    return round(time.time() * 1000)


class timerThread(QThread):
    timeoutSignal=pyqtSignal()
    timeoutTime=2000

    def __init__(self):
        super().__init__()
        self.timer=QTimer()
        self.timer.timeout.connect(self.timeoutFunction)
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.moveToThread(self)
        

    def stopTimer(self):
        self.timer.stop()
        
    def setTimeout(self,timeout):
        timerThread.timeoutTime = timeout

    def timeoutFunction(self):
        print("TIMEOUT BOLUS TIMER")
        Logger.q.put(("INFO","TIMEOUT BOLUS TIMER"))
        self.timeoutSignal.emit()


    def run(self):
        self.setPriority(QThread.HighestPriority)
        print("Started BOLUS TIMER {}".format(self.timeoutTime))
        
        Logger.q.put(("INFO","Started BOLUS TIMER {}ms delay".format(self.timeoutTime)))
        
        self.timer.start(self.timeoutTime)
        loop = QEventLoop()
        loop.exec_()