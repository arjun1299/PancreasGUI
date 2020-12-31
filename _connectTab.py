import os

"""
    Tab 1- connect tab
"""
    
class connectTab(object):


    def init_connectTab(self):
        self.check=self.ui.checkBox
        self.chk()
        self.check.clicked.connect(self.chk)
        #dropdown
        self.dropdown=self.ui.comboBox
        #scan button
        self.scanButton=self.ui.scanButton
        self.scanButton.clicked.connect(self.scanPort)
        #connect button
        self.connectButton=self.ui.connectButton
        self.connectButton.setEnabled(False)
        self.connectButton.clicked.connect(self.connectPort)
        

    def isConnectedBLE(self):
        #check for heartbeat here
        pass

        return 0

    def isConnectedReciever(self):
        #checks if bluetooth reciever is connected
        if(os.system("hcitool scan")== 256):
            return 0
        return 1


    def chk(self):
        #enable tabs
        #se lf.ui.tabWidget.setTabEnabled(1,self.isConnectedBLE())
        #self.ui.tabWidget.setTabEnabled(2,self.isConnectedBLE())
        pass


    def connectPort(self):
        if(self.dropdown.currentText()):
            self.port=self.dropdown.currentText()
            
            """
            #add logic to pair with BLE
            """

            print("Connected to:"+self.dropdown.currentText())
    
    def scanPort(self):
        
        print("Scanning...")
        
        self.ongoing="Scanning"
        self.updateStatus()
        
        if(self.isConnectedReciever):
            self.updateStatus()
            return 0
        
        cmd=os.popen("hcitool scan")
        
        comlist = cmd.read()
        
        comlist = comlist.split('\n')
        
        #the last element is empty 
        comlist.pop()

        connected = []
        self.dropdown.clear()
        for element in comlist:
            connected.append(element.device)
            self.dropdown.addItem(element.device)
        
        self.connectButton.setEnabled(True)
