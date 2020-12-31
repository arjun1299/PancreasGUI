"""
Tab-3
Command tab
"""
class commandTab(object):

    def init_commandTab(self):
        self.sendButton=self.ui.SendButton
        self.cmdTxt=self.ui.cmdTxt
        self.outTxt=self.ui.outTxt
        self.sendButton.clicked.connect(self.sendButtonClick)

    def sendButtonClick(self):
        self.sendCommand(self.cmdTxt.toPlainText())
        self.outTxt.appendPlainText(self.cmdTxt.toPlainText())
        
    def sendCommand(self,text):
        print("Sending:"+text)
        ser=serial.Serial(self.port)
        text=bytes(text,'utf-8')
        ser.write(text)
        ser.close()
        

