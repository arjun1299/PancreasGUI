
"""
Tab-2
Priming
"""

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class primingTab(object):
    def init_primingTab(self):
        #start prime
        self.startPrimeBtn=self.ui.startPrimeBtn
        self.startPrimeBtn.clicked.connect(self.enablePriming)
        
    
        #rotate
        self.rotateBtn=self.ui.rotateBtn
        self.rotateBtn.setEnabled(False)
        self.countTxt=self.ui.countTxt
        self.rotateBtn.clicked.connect(self.rotate)

        
        #clutch
        self.toggleClutchBtn=self.ui.toggleClutchBtn
        self.toggleClutchBtn.setEnabled(False)

        self.toggleClutchBtn.setText("Gear")
        
        self.toggleClutchBtn.clicked.connect(self.engageClutch)

        #fixed prime
        self.fixedPrimeBtn=self.ui.fixedPrimeBtn  
        self.fixedPrimeBtn.setEnabled(False)

        #finish
        self.finishPrimeBtn=self.ui.finishPrimeBtn
        self.finishPrimeBtn.clicked.connect(self.stopPriming)


    def enablePriming(self):
        self.rotateBtn.setEnabled(True)
        self.toggleClutchBtn.setEnabled(True)
        self.fixedPrimeBtn.setEnabled(True)
        self.ongoing="Priming"
        self.showDialog("Prime")
        self.updateStatus()

    def rotate(self):
        #do one rotation
        self.primingRotations+=1
        
        #self.countTxt.setFontPointSize(20)
        self.countTxt.setText(str(self.primingRotations))
        

    def engageClutch(self):
        if self.clutch== False:
            self.clutchBtn.setText("Ratchet")
            self.clutch=True
            self.sender.q.put("IPPC\r")
            
        else:
            self.clutchBtn.setText("Gear")
            self.clutch=False
            self.sender.q.put("IPDC\r")
        
        self.updateStatus()
            

    def stopPriming(self):
        self.ui.tabWidget.setCurrentIndex((self.ui.tabWidget.currentIndex()+1))

        pass
