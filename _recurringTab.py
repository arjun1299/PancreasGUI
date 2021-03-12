"""
Tab-4
Recurring commands  tab
"""
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer,QThreadPool,QThread


from basicui import Ui_MainWindow
from bleOperations import *
from _bolusTesting import current_milli_time,timerThread
import time


class recurringTab(object):
    
    def init_recurringTab(self):
        
        
        self.basalBtn=self.ui.basalBtn
        self.basalBtn.clicked.connect(self.enableBasalMode)

        

        self.bolusBtn=self.ui.bolusBtn
        self.bolusBtn.clicked.connect(self.enableBolusMode)

        
        self.startDoseBtn=self.ui.startDoseBtn
        self.startDoseBtn.clicked.connect(self.startDeliveryHandler)
        self.doseTxt=self.ui.doseTxt
        self.doseLbl=self.ui.doseLbl
        self.doseTxt.setVisible(True)
        self.doseLbl.setVisible(True)



        self.pulseDelayTxt= self.ui.pulseDelayTxt
        self.pulseDelayLbl= self.ui.pulseDelayLbl
        self.pulseDelayTxt.setVisible(False)
        self.pulseDelayLbl.setVisible(False)

        self.deliveryAmtTxt= self.ui.deliveryAmtTxt
        self.deliveryAmtLbl= self.ui.deliveryAmtLbl
        self.deliveryAmtTxt.setVisible(False)
        self.deliveryAmtLbl.setVisible(False)

        self.deliveryType=None
        self.basalResume=False #flag used for resuming basal delivery after completion of bolus
        """
        Basal delivery paramters
        """
        self.basalRate=0
        self.basalTimer=timerThread()
        self.basalTimer.timeoutSignal.connect(self.basalDose)
        



    
    def basalDose(self):
        
        #if self.showDialog("BASAL dose {} Iu/hr".format(self.basalTxt.toPlainText())) == QMessageBox.Ok:
        if self.showDialog("BASAL mode") == QMessageBox.Ok:
            self.deliveryType="Basal"
            self.startDoseBtn.setEnabled(True)
        else:
            self.basalBtn.checkStateSet(False)
    
    def enableBasalMode(self):
        #Toggling element visibility
        if self.showDialog("BASAL mode") == QMessageBox.Ok:
            self.deliveryType="Basal"
            self.doseTxt.setVisible(True)
            self.doseLbl.setVisible(True)
            self.pulseDelayTxt.setVisible(False)
            self.pulseDelayLbl.setVisible(False)
            self.deliveryAmtTxt.setVisible(False)
            self.deliveryAmtLbl.setVisible(False)     

    
    def enableBolusMode(self):
        if self.showDialog("BOLUS mode") == QMessageBox.Ok:
            if self.deliveryType=="Basal":
                self.basalResume=True

            self.deliveryType="Bolus"
            self.doseTxt.setVisible(False)
            self.doseLbl.setVisible(False)
            self.pulseDelayTxt.setVisible(True)
            self.pulseDelayLbl.setVisible(True)
            self.deliveryAmtTxt.setVisible(True)
            self.deliveryAmtLbl.setVisible(True)


    
    """def bolusDose(self):

        if self.showDialog("BOLUS mode") == QMessageBox.Ok:
            
            self.startDoseBtn.setEnabled(True)

        else:
            self.basalBtn.checkStateSet(False)
    
    def startDose(self):
  
            if self.showDialog("{} dose {} Iu/hr".format(self.deliveryType,self.doseTxt.toPlainText())) == QMessageBox.Ok:
                self.dose=self.doseTxt.toPlainText()
                self.updateStatus()"""

    def startBasalDelivery(self):
        
        self.basalRate=int(self.doseTxt.toPlainText())
        """
        Delivery amount x
        x/0.05 actuations will have to be done
        3600*1000/x*0.05 gives the milliseconds
        """
        self.timeBetweenPulses=(3600*1000/self.basalRate*0.05)
        self.insulonCompleteFlag=True
        self.ongoingDeliveryFlag=True
        self.heartBeatChecker.heartBeatSenderTimer.stop()
        self.heartBeatChecker.heartBeatRecieverTimer.stop()
        
        self.cycleNumber=0

        """Steps:
        1. Send HB
        2. Recieve reply HB
        3. Send IN based on  heartbeat response
        """
        print("Starting Basal Delivery")
        
        Logger.q.put(("WARNING","Starting Basal Delivery with rate {}IU/hr ".format(self.basalRate)))
        self.showWarning("Start Basal Delivery with rate {}IU/hr ?".format(self.basalRate))
        self.completedDose=0
        #self.timeBetweenPulses=2000
        self.basalTimer.setTimeout(self.timeBetweenPulses)
        self.basalTimer.start()
        self.basalTimer.setPriority(QThread.HighestPriority)
    
    def setInsulonCompleteFlag(self,status):
        self.insulonCompleteFlag= status

    def resetHandler(self,encoderValue):
        Logger.q.put(("INFO","Encoder value: {}".format(encoderValue)))

        if self.deliveryType=="Basal":
            self.resetBasalTimer()
        elif self.deliveryType=="Bolus":
            self.resetBolusTimer()

    def startDeliveryHandler(self,encoderValue):
        if self.deliveryType=="Basal":
            self.startBasalDelivery()
        elif self.deliveryType=="Bolus":
            self.startBolusDelivery()

    def resetBasalTimer(self):
        
        """Resets the basal timer if the delivery target has not been reached

        :param timeDelay: String, it has to be converted to an int before
        :type timeDelay: string
        """
        print("RESET BASAL TIMER")
        #Logger.q.put(("INFO","Encoder value: {}".format(encoderValue)))
        
        if(self.ongoingDeliveryFlag==False):
            return


        self.insulonCompleteFlag=True
        self.cycleNumber+=1            
        Logger.q.put(("WARNING","Resetting basal delivery timer,{} cycles complete".format(self.cycleNumber)))
        
        print("Reset Basal timer")

        
        #self.bolusTimer.start()
        
        #This method uses delay given by the device
        #self.bolusTimer.start(abs(int(self.timeBetweenPulses-int(timeDelay))))
        print("Time Delay: ")
        
        print(self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))
        
        #time compensation
        self.insulonEndTime=current_milli_time()
        timediff=(self.insulonEndTime-self.insulonStartTime)+self.averageCorrection
        
        self.basalTimer.timeoutTime=self.timeBetweenPulses-timediff
        self.basalTimer.start()
        self.basalTimer.setPriority(QThread.HighestPriority)

    def stopBasalDelivery():
        self.showWarning("Stop Basal Delivery?")
        Logger.q.put(("WARNING","Stopped Basal Delivery"))
        self.basalTimer.timerRun=False
        self.basalTimer.quit()
        #self.bolusTimer.stop()

    def basalDose(self):
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
        self.logic.pq.put((1,"INSHB"))
        self.prevTime=self.insulonStartTime
        self.insulonCompleteFlag=False
        

