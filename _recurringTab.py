"""
Tab-4
Recurring commands  tab
"""
from PyQt5.QtWidgets import  QMessageBox

class recurringTab(object):
    
    def init_recurringTab(self):
        
        
        self.basalBtn=self.ui.basalBtn
        self.basalBtn.clicked.connect(self.enableBasalMode)

        

        self.bolusBtn=self.ui.bolusBtn
        self.bolusBtn.clicked.connect(self.enableBolusMode)

        
        self.startDoseBtn=self.ui.startDoseBtn
        self.doseTxt=self.ui.doseTxt
        self.doseLbl=self.ui.doseLbl
        self.doseTxt.setVisible(True)
        self.doseLbl.setVisible(True)

        #self.startDoseBtn.setEnabled(False)
        #self.startDoseBtn.clicked.connect(self.startDose)
        self.startDoseBtn.clicked.connect(self.startBolusDelivery)     

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
    
    def basalDose(self):
        
        #if self.showDialog("BASAL dose {} Iu/hr".format(self.basalTxt.toPlainText())) == QMessageBox.Ok:
        if self.showDialog("BASAL mode") == QMessageBox.Ok:
            self.deliveryType="Basal"
            self.startDoseBtn.setEnabled(True)
        else:
            self.basalBtn.checkStateSet(False)
    
    def enableBasalMode(self):
        #Toggling element visibility
        self.deliveryType="Basal"
        self.doseTxt.setVisible(True)
        self.doseLbl.setVisible(True)
        self.pulseDelayTxt.setVisible(False)
        self.pulseDelayLbl.setVisible(False)
        self.deliveryAmtTxt.setVisible(False)
        self.deliveryAmtLbl.setVisible(False)
    
    def enableBolusMode(self):
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
            self.basalBtn.checkStateSet(False)"""
    
    def startDose(self):
  
            if self.showDialog("{} dose {} Iu/hr".format(self.deliveryType,self.doseTxt.toPlainText())) == QMessageBox.Ok:
                self.dose=self.doseTxt.toPlainText()
                self.updateStatus()