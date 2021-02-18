from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer,QThreadPool,QThread

from basicui import Ui_MainWindow
from bleOperations import *
import time

class bolusTestingTab(object):
    def init_bolusTestingTab(self):
        #start prime
        self.startPrimeBtn=self.ui.startPrimeBtn
        self.startPrimeBtn.clicked.connect(self.enablePriming)
        self.pulseDelayTxt= self.ui.pulseDelayTxt
        self.deliveryAmtTxt= self.ui.deliveryAmtTxt

        self.startBolusBtn=self.ui.startBolusBtn
        self.startBolusBtn.clicked.connect(self.startBolusDelivery)
        self.stopBolusBtn=self.ui.stopBolusBtn

        self.bolusTimer=QTimer()
        self.bolusTimer.timeout.connect(self.bolusDose)
        
        self.completedDose=0
        self.timeBetweenPulses=0

        #Time duration  monitoring
        self.insulonStartTime=0
        self.insulonEndTime=0
    
    def startBolusDelivery(self):
        
        print("Starting Bolus Delivery")
        Logger.q.put("WARNING","Starting Bolus Delivery")
        self.timeBetweenPulses=int(self.pulseDelayTxt.toPlainText())
        self.deliveryAmount=int(self.deliveryAmtTxt.toPlainText())
        self.showWarning("Start Bolus Delivery with duration {} for {}IU ?".format(self.timeBetweenPulses,self.deliveryAmount))
        self.completedDose=0
        #self.timeBetweenPulses=2000
        self.bolusTimer.start(self.timeBetweenPulses)
    
    def resetBolusTimer(self,timeDelay):
        """Resets the bolus timer if the delivery target has not been reached

        :param timeDelay: String, it has to be converted to an int before
        :type timeDelay: string
        """
        if self.deliveryAmount>0:
            self.deliveryAmount-=1 #decrease by amount consumed in 1 rotation
            timeDelay=float(timeDelay)
            print("Reset Bolus timer")
            
            
            self.bolusTimer.stop()
            self.insulonEndTime=current_milli_time()
            #This method uses delay given by the device
            #self.bolusTimer.start(abs(int(self.timeBetweenPulses-int(timeDelay))))
            print("Time Delay: ")
            print(self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))
            self.bolusTimer.start(self.timeBetweenPulses-(self.insulonEndTime-self.insulonStartTime))
            
        else:
            self.bolusTimer.stop()
            Logger.q.put("WARNING","Completed Bolus Delivery")

    def stopBolusDelivery():
        self.showWarning("Stop Bolus Delivery?")
        Logger.q.put("WARNING","Stopped Bolus Delivery")
        self.bolusTimer.stop()


        
    
    def bolusDose(self):
        print("Sent bolus dose")
        self.sender.q.put("IPIN\r")

        #Start timer
        self.insulonStartTime=current_milli_time()

        
def current_milli_time():
    return round(time.time() * 1000)