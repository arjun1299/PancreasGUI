"""
Tab-4
Recurring commands  tab
"""
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer,QThreadPool,QThread,QTime
from PyQt5.QtCore import *
import PyQt5.QtCore


from basicui import Ui_MainWindow
from bleOperations import *
from _bolusTesting import current_milli_time,timerThread
import time


class recurringTab(object):
    
    def init_recurringTab(self):
        
        
        self.basalBtn=self.ui.basalBtn
        self.basalBtn.clicked.connect(self.enableBasalMode)

        self.basalPauseLbl=self.ui.basalPauseLbl
        self.basalPauseLbl.setVisible(False)
        

        self.bolusBtn=self.ui.bolusBtn
        self.bolusBtn.clicked.connect(self.enableBolusMode)

        self.outTxt=self.ui.outTxt

        
        self.startDoseBtn=self.ui.startDoseBtn
        self.startDoseBtn.clicked.connect(self.startDeliveryHandler)
        self.doseTxt=self.ui.doseTxt
        self.doseLbl=self.ui.doseLbl
        self.doseTxt.editingFinished.connect(self.basalRateChanged)
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

        self.buttonGroup=QButtonGroup()
        self.buttonGroup.addButton(self.basalBtn)
        self.buttonGroup.addButton(self.bolusBtn)

        self.basalProfileBtn=self.ui.basalProfileBtn
        self.basalProfileBtn.clicked.connect(self.showInput)

        """
        Basal profile parameters
        """
        self.profileFrame=self.ui.profileFrame
        self.profileFrame.setVisible(False)

        self.setProfileBtn=self.ui.setProfileBtn
        self.setProfileBtn.clicked.connect(self.hideInput)
        self.basalProfileTimes=[]
        self.basalProfileAmounts=[]
        self.index=0#keeps track of which delivery is ongoing

    def showInput(self):
        """This is for the basal profile mode
        """
        self.profileFrame.setVisible(True)

    def hideInput(self):
        """This function is for after the apply button is clicked on the basal profile menu
        """
        self.profileFrame.setVisible(False)
        self.basalProfileAmounts=[self.ui.profileRate_1.text(),self.ui.profileRate_2.text(),self.ui.profileRate_3.text(),self.ui.profileRate_4.text(),self.ui.profileRate_5.text(),self.ui.profileRate_6.text()]
        temp=self.basalProfileAmounts
        self.basalProfileAmounts=[]
        for i in temp:
            if i!='':
                self.basalProfileAmounts.append(float(i))
        self.basalProfileTimes=[self.ui.timeEdit_1.time(),self.ui.timeEdit_2.time(),self.ui.timeEdit_3.time(),self.ui.timeEdit_4.time(),self.ui.timeEdit_5.time(),self.ui.timeEdit_6.time()]
        print(self.basalProfileAmounts)
        print(self.basalProfileTimes)

    def basalRateChanged(self):
        """On a change of rate this is finished
        """
        self.showDialog("Change Basal rate to {}?".format(self.doseTxt.text()))

    
    def basalDose(self):
        """On clicking basal's radio button this function will be executed, ensures radio buttons work as expected
        """
        
        #if self.showDialog("BASAL dose {} Iu/hr".format(self.basalTxt.toPlainText())) == QMessageBox.Ok:
        if self.showDialog("Switch to BASAL mode") == QMessageBox.Ok:
            self.deliveryType="Basal"
            self.startDoseBtn.setEnabled(True)
        else:
            self.buttonGroup.setExclusive(False)
            self.basalBtn.setChecked(False)
            self.buttonGroup.setExclusive(True)
    
    def enableBasalMode(self):
        """Enables basal mode, sets appropriate flags and makes the required elements visible
        """
        #Toggling element visibility
        if self.showDialog("Switch to BASAL mode?") == QMessageBox.Ok:
            self.deliveryType="Basal"
            self.doseTxt.setVisible(True)
            self.doseLbl.setVisible(True)
            self.pulseDelayTxt.setVisible(False)
            self.pulseDelayLbl.setVisible(False)
            self.deliveryAmtTxt.setVisible(False)
            self.deliveryAmtLbl.setVisible(False)     
        else:
            
            self.buttonGroup.setExclusive(False)
            self.basalBtn.setChecked(False)
            if self.deliveryType=="Bolus":
                self.bolusBtn.setChecked(True)
            self.buttonGroup.setExclusive(True)
    
    def enableBolusMode(self):
        """Enables bolus mode, sets appropriate flags and makes the required elements visible
        """

        if self.showDialog("Switch to BOLUS mode?") == QMessageBox.Ok:  
            if self.deliveryType=="Basal":
                self.basalResume=True
            
            if self.basalResume==True:
                self.basalPauseLbl.setVisible(True)

            self.deliveryType="Bolus"
            self.doseTxt.setVisible(False)
            self.doseLbl.setVisible(False)
            self.pulseDelayTxt.setVisible(True)
            self.pulseDelayLbl.setVisible(True)
            self.deliveryAmtTxt.setVisible(True)
            self.deliveryAmtLbl.setVisible(True)
        else:
            
            self.buttonGroup.setExclusive(False)
            self.bolusBtn.setChecked(False)
            if self.deliveryType=="Basal":
                self.basalBtn.setChecked(True)
            self.buttonGroup.setExclusive(True)


    
    """def bolusDose(self):

        if self.showDialog("BOLUS mode") == QMessageBox.Ok:
            
            self.startDoseBtn.setEnabled(True)

        else:
            self.basalBtn.checkStateSet(False)
    
    def startDose(self):
  
            if self.showDialog("{} dose {} Iu/hr".format(self.deliveryType,self.doseTxt.toPlainText())) == QMessageBox.Ok:
                self.dose=self.doseTxt.toPlainText()
                self.updateStatus()"""
    def basalCalc(self,basalRate):
        """
        Delivery rate x
        x/0.05 actuations will have to be done
        3600*1000/x*0.05 gives the milliseconds
        """
        self.timeBetweenPulses=(3600*1000/basalRate*0.05)

    def startBasalDelivery(self):
        """
        Function exected on the start of basal delivery
        1. Send HB
        2. Recieve reply HB
        3. Send IN based on  heartbeat response
        """
        self.deliveryType="Basal"
        self.basalRate=int(self.doseTxt.text())

        self.basalCalc(self.basalRate)

        self.ongoingDeliveryFlag=True
        self.basalPauseLbl.setVisible(False)
        self.heartBeatChecker.heartBeatSenderTimer.stop()
        self.heartBeatChecker.heartBeatRecieverTimer.stop()
        
        self.cycleNumber=0

        """Steps:
        1. Send HB
        2. Recieve reply HB
        3. Send IN based on  heartbeat response
        """
        print("Starting Basal Delivery")
        
        
        if self.showDialog("Start Basal Delivery with rate {}IU/hr ?".format(self.basalRate))==QMessageBox.Ok:
            Logger.q.put(("WARNING","Starting Basal Delivery with rate {}IU/hr ".format(self.basalRate)))
            timeStamp=datetime.datetime.now()
            timeStamp = timeStamp.strftime("%H:%M:%S")
            self.outTxt.appendPlainText(timeStamp+"-> "+"Starting Basal Delivery with rate {}IU/hr".format(self.basalRate))
            self.completedDose=0
            #self.timeBetweenPulses=2000
            self.basalTimer.setTimeout(self.timeBetweenPulses)
            self.basalTimer.start()
            self.basalTimer.setPriority(QThread.HighestPriority)
            
    

    def resetHandler(self,encoderValue):
        """On a timer reset the reset handler resets the approprate timer

        :param encoderValue: Value obtained along with the execution of the IN command
        :type encoderValue: int/str
        """
        Logger.q.put(("INFO","Encoder value: {}".format(encoderValue)))

        if self.deliveryType=="Basal":
            self.resetBasalTimer()
        elif self.deliveryType=="Bolus":
            self.resetBolusTimer()

    def startDeliveryHandler(self,encoderValue):
        """On pressing of start, this function calls the appropriate function

        :param encoderValue: [description]
        :type encoderValue: [type]
        """
        if self.checkActuationLimit():
            self.logic.allowActuation=True
        else:
            self.logic.allowActuation=False
        if self.deliveryType=="Basal":
            self.startBasalDelivery()
        elif self.deliveryType=="Bolus":
            self.startBolusDelivery()
        elif self.deliveryType==None:
            self.showError("Pick a delivery mode")

    def chkTime(self):
        """
        This is for basal profiles
        """
        if len(self.basalProfileTimes)==0:
            self.index=-1
            return
        #Switch to new index
        if len(self.basalProfileTimes)==1:
            self.index=0
            return
        if not self.index+1 >= len(self.basalProfileAmounts):
            if not self.basalProfileTimes[self.index]<=QTime.currentTime()<=self.basalProfileTimes[self.index+1]:
                """When index is 0, then it may be the next day.
                    We check if its back to the same hour, this way we can check if the greater than value of time is of the same day or the next
                """
                self.index+=1
        elif self.basalProfileTimes[self.index]>=QTime.currentTime():
            if self.basalProfileTimes[0]<=QTime.currentTime():
            #this will indicate that it has gone to the next day and it is past the first time, indicating a full cycle complete
                self.index=0
            
           


    def resetBasalTimer(self):
        
        """Resets the basal timer if the delivery target has not been reached

        :param timeDelay: String, it has to be converted to an int before
        :type timeDelay: string
        """
        print("RESET BASAL TIMER")
        #Logger.q.put(("INFO","Encoder value: {}".format(encoderValue)))
        
        if(self.ongoingDeliveryFlag==False):
            return

        self.chkTime()
        self.basalRate=float(self.basalProfileAmounts[self.index])
        self.basalCalc(self.basalRate)
        

        self.insulonCompleteFlag=True
        self.cycleNumber+=1            
        Logger.q.put(("WARNING","Resetting basal delivery timer,{} cycles complete".format(self.cycleNumber)))
        
        print("Reset Basal timer")

        print("Time Delay: ")
        
        print(self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))
        
        #time compensation
        self.insulonEndTime=current_milli_time()
        timediff=(self.insulonEndTime-self.insulonStartTime)+self.averageCorrection
        
        self.basalTimer.timeoutTime=self.timeBetweenPulses-timediff
        self.basalTimer.start()
        self.basalTimer.setPriority(QThread.HighestPriority)

    def stopBasalDelivery():
        """On an attempt to stop basal delivery, this function ensure safe stop and quitting of timer threads
        """
        self.showWarning("Stop Basal Delivery?")
        Logger.q.put(("WARNING","Stopped Basal Delivery"))
        self.basalTimer.timerRun=False
        self.basalTimer.quit()
        #self.bolusTimer.stop()

    def basalDose(self):
        """
        A basal dose gets sent via this function, the time gap between deliveries is logged
        """
        #if the previous dose is complete only then send the next should start
        #if self.insulonCompleteFlag==True:
        self.insulonStartTime=current_milli_time()
        print("Sent bolus dose",self.insulonStartTime)
        timeStamp=datetime.datetime.now()
        ts = timeStamp.strftime("%H:%M:%S")
        self.outTxt.appendPlainText(ts+"-> "+"Sent basal dose, next dose at {}".format(timeStamp+ datetime.timedelta(milliseconds=self.timeBetweenPulses)))
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

        

