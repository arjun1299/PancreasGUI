
"""
Tab-2
Priming
"""
class primingTab(object):
    def init_primingTab(self):
        #start prime
        self.startPrime=self.ui.startPrime
        self.startPrime.clicked.connect(self.enablePriming)
        #rotate
        self.rotateBtn=self.ui.rotateBtn
        self.rotateBtn.setEnabled(False)

        #stop
        self.stopBtn=self.ui.stopBtn
        self.stopBtn.setEnabled(False)

    def enablePriming(self):
        self.rotateBtn.setEnabled(True)
        self.stopBtn.setEnabled(True)
        self.ongoing="Priming"
        self.updateStatus()

    def rotate(self):
        #do one rotation
        pass


    def stop(self):
        #do one rotation
        pass
    