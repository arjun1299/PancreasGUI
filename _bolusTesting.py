from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer,QThreadPool,QThread

from basicui import Ui_MainWindow
from bleOperations import *
import time


t1=0
t2=0

class bolusTestingTab(object):
    def __init__(self):
        super().__init__()

    def init_bolusTestingTab(self):
        #start prime
        self.ongoingDeliveryFlag=False
        self.averageCorrection=0
        self.startPrimeBtn=self.ui.startPrimeBtn
        self.startPrimeBtn.clicked.connect(self.enablePriming)
        self.pulseDelayTxt= self.ui.pulseDelayTxt
        self.deliveryAmtTxt= self.ui.deliveryAmtTxt

        self.startBolusBtn=self.ui.startBolusBtn
        self.startBolusBtn.clicked.connect(self.startBolusDelivery)
        self.stopBolusBtn=self.ui.stopBolusBtn
        self.cycleNumber=0

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

        self.pulseDelayTxt.editingFinished.connect(self.timeBetweenPulsesChanged)
        self.deliveryAmtTxt.editingFinished.connect(self.bolusDeliveryAmountChanged)


    def timeBetweenPulsesChanged(self):
        self.showDialog("Change Bolus inteval to {}?".format(self.pulseDelayTxt.text()))

    def bolusDeliveryAmountChanged(self):
        self.showDialog("Change Basal rate to {}?".format(self.deliveryAmtTxt.text()))
    
    def startBolusDelivery(self):
        self.deliveryType="Bolus"

        self.ongoingDeliveryFlag=True
        self.heartBeatChecker.heartBeatSenderTimer.stop()
        self.heartBeatChecker.heartBeatRecieverTimer.stop()
        
        
        self.cycleNumber=0
        """Steps:
        1. Send HB
        2. Recieve reply HB
        3. Send IN based on  heartbeat response
        """
        print("Starting Bolus Delivery")
        
        self.timeBetweenPulses=int(self.pulseDelayTxt.text())
        self.deliveryAmount=float(self.deliveryAmtTxt.text())
        Logger.q.put(("WARNING","Starting Bolus Delivery with duration {} for {}IU ".format(self.timeBetweenPulses,self.deliveryAmount)))
        if self.showDialog("Start Bolus Delivery with duration {} for {}IU ?".format(self.timeBetweenPulses,self.deliveryAmount))==QMessageBox.Ok:
            self.completedDose=0
            #self.timeBetweenPulses=2000
            self.bolusTimer.setTimeout(self.timeBetweenPulses)
            #self.bolusTimer.finished.connect(self.completedBolusRegime)
            self.bolusTimer.start()
            self.bolusTimer.setPriority(QThread.HighestPriority)
            timeStamp=datetime.datetime.now()
            timeStamp = timeStamp.strftime("%H:%M:%S")
            self.outTxt.appendPlainText(timeStamp+"-> "+"Starting Bolus Delivery with duration {} for {}IU ".format(self.timeBetweenPulses,self.deliveryAmount))
            self.outTxt.appendPlainText("Remaining Time: "+str(self.timeBetweenPulses/1000*self.deliveryAmount/0.05)+"seconds")



    def resetBolusTimer(self):
        
        """Resets the bolus timer if the delivery target has not been reached

        :param timeDelay: String, it has to be converted to an int before
        :type timeDelay: string
        """
        #Logger.q.put(("INFO","Encoder value: {}".format(encoderValue)))
        if(self.ongoingDeliveryFlag==False):
            return
        if self.deliveryAmount>0:
                

                self.deliveryAmount=round(self.deliveryAmount-0.05,2) #decrease by amount consumed in 1 rotation
               
                self.cycleNumber+=1
                
                Logger.q.put(("WARNING","Resetting bolus delivery timer,{} remaining".format(self.deliveryAmount)))
                timeStamp=datetime.datetime.now()
                timeStamp = timeStamp.strftime("%H:%M:%S")
                self.outTxt.appendPlainText(timeStamp+"-> "+"Sent bolus dose, {} remaining".format(self.deliveryAmount))
                self.outTxt.appendPlainText("Remaining Time: "+str(round(self.timeBetweenPulses/1000*self.deliveryAmount/0.05,2))+"seconds")

                print("Reset Bolus timer")

                
                #self.bolusTimer.start()
                
                #This method uses delay given by the device
                #self.bolusTimer.start(abs(int(self.timeBetweenPulses-int(timeDelay))))
                print("Time Delay: ")
                
                print(self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))
                #self.bolusTimer.start(self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))#self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))
                #self.bolusTimer.setTimeout(self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))#self.timeBetweenPulses)
                
                #self.deliveryAmount+=1

                #constant time delay
                self.insulonEndTime=current_milli_time()
                timediff=(self.insulonEndTime-self.insulonStartTime)+self.averageCorrection
                
                #self.bolusTimer.setTimeout(self.timeBetweenPulses-timediff)
                #self.bolusTimer.quit()
                self.bolusTimer.timeoutTime=self.timeBetweenPulses-timediff
                self.bolusTimer.start()
                self.bolusTimer.setPriority(QThread.HighestPriority)

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
            self.completedBolusRegime()

    def stopBolusDelivery():
        self.showWarning("Stop Bolus Delivery?")
        Logger.q.put(("WARNING","Stopped Bolus Delivery"))
        self.bolusTimer.timerRun=False
        self.bolusTimer.quit()
        #self.bolusTimer.stop()

    def bolusDose(self):
        #if the previous dose is complete only then send the next should start
        #if self.insulonCompleteFlag==True:
        self.insulonStartTime=current_milli_time()
        print("Sent bolus dose",self.insulonStartTime)

        timeGap=self.insulonStartTime-self.prevTime
        print("Time difference::::::",(timeGap))
        #time.sleep(0.0005)
        Logger.q.put(("INFO","Time difference between deliveries ::::{}".format(timeGap)))
        #To avoid compensating for the first delivery
        """Every alternate cycle(even cycles are a correction for the previous cycle's errror and tries to keep the average error to 0)
        """
        
        if(timeGap<self.timeBetweenPulses+500) and self.cycleNumber%2==0 :
            #self.averageCorrection=((timeGap-self.timeBetweenPulses)+self.averageCorrection)/2
            self.averageCorrection=(timeGap-self.timeBetweenPulses)
        else:
            self.averageCorrection=0
        print("Average Correction:",self.averageCorrection)
        
        #self.sender.q.put("IPIN\r")
        self.logic.pq.put((1,"INSHB"))
        #self.uart_service.write("IPIN\r".encode("utf-8"))
        self.prevTime=self.insulonStartTime

        
        #else:
        #    Logger.q.put(("ERROR","Response too slow, Skipping delivery"))


        #Start timer
    def completedBolusRegime(self):  
        self.heartBeatChecker.heartBeatSenderTimer.stop()
        self.heartBeatChecker.heartBeatRecieverTimer.stop()

        if  self.basalResume == True:
            self.startBasalDelivery()
            self.basalPauseLbl.setVisible(False)
        else:
            self.heartBeatChecker.heartBeatSenderTimer.start()
        
        
def current_milli_time():
    return round(time.time() * 1000)

"""
class timerThread(QThread):
    timeoutSignal=pyqtSignal()
    timeoutTime=2000

    def __init__(self):
        super().__init__()
        self.timer=QTimer()
        self.timer.timeout.connect(self.timeoutFunction)
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.moveToThread(self)
        self.timerStopFlag=False
        

    def stopTimer(self):
        self.timer.stop()
        
    def setTimeout(self,timeout):
        timerThread.timeoutTime = timeout

    def timeoutFunction(self):
        print("TIMEOUT BOLUS TIMER{}".format(current_milli_time()))
        Logger.q.put(("INFO","TIMEOUT BOLUS TIMER"))
        self.timeoutSignal.emit()


    def run(self):
        global t2
        t2=current_milli_time()
        self.setPriority(QThread.HighestPriority)
        print("Started BOLUS TIMER {}".format(self.timeoutTime))
        print("Time taken to start timer:")
        
        Logger.q.put(("INFO","Started BOLUS TIMER {}ms delay".format(self.timeoutTime)))
        
        self.timer.start(timerThread.timeoutTime)
        loop = QEventLoop()
        loop.exec_()
""" 

class timerThread(QThread):
    timeoutSignal=pyqtSignal()

    def __init__(self):
        super().__init__()
        self.targetTime=0
        self.timeoutTime=0
        self.timerRun=False

        

    def setTimeout(self,timeout):
        self.timeoutTime = timeout
        
        
    def run(self):
        self.setPriority(QThread.HighestPriority)
        self.targetTime = self.timeoutTime*1000000+time.time_ns()
        print("----------Started BOLUS TIMER {}".format(self.timeoutTime))
        print("Time taken to start timer:")
        self.timerRun=True

        while self.timerRun==True:
            if time.time_ns()>=self.targetTime:
                self.timeoutSignal.emit()
                print("TIMEOUT BOLUS TIMER{}".format(current_milli_time()))
                Logger.q.put(("INFO","TIMEOUT BOLUS TIMER"))
                self.timerRun=False
                break
            #time.sleep(0.0005)

