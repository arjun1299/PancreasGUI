"""
Tab-4
Recurring commands  tab
"""
from PyQt5.QtWidgets import  QMessageBox

class recurringTab(object):
    
    def init_recurringTab(self):
        
        self.basalBtn=self.ui.basalBtn
        self.basalBtn.clicked.connect(self.basalDose)

        

        self.bolusBtn=self.ui.bolusBtn
        self.bolusBtn.clicked.connect(self.bolusDose)

        
        self.startDoseBtn=self.ui.startDoseBtn
        self.doseTxt=self.ui.doseTxt

        self.startDoseBtn.setEnabled(False)
        self.startDoseBtn.clicked.connect(self.startDose)


        
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
            
            
            

    
    """def bolusDose(self):

        if self.showDialog("BOLUS mode") == QMessageBox.Ok:
            
            self.startDoseBtn.setEnabled(True)

        else:
            self.basalBtn.checkStateSet(False)"""
    
    def startDose(self):
  
            if self.showDialog("{} dose {} Iu/hr".format(self.deliveryType,self.doseTxt.toPlainText())) == QMessageBox.Ok:
                self.dose=self.doseTxt.toPlainText()
                self.updateStatus()