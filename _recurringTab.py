"""
Tab-4
Recurring commands  tab
"""

class recurringTab(object):
    
    def init_recurringTab(self):
        self.setButton=self.ui.SetButton
        self.basalBtn=self.ui.basalBtn
        self.basalTxt=self.ui.basalTxt
        self.basalBtn.clicked.connect(self.basalDose)
        

        #self.bolusBtn=self.ui.bolusBtn
        #self.bolusTxt=self.ui.bolusTxt

        #self.bolusBtn.clicked.connect(self.bolusDose)

        

        self.setButton.clicked.connect(self.reSendCommand)
        
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
        self.showDialog("Basal")
    
    def bolusDose(self):
        self.showDialog("Basal")
