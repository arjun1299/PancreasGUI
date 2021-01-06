
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
        self.startPrime=self.ui.startPrime
        self.startPrime.clicked.connect(self.enablePriming)
    
        #rotate
        self.rotateBtn=self.ui.rotateBtn
        self.rotateBtn.setEnabled(False)
        self.countTxt=self.ui.countTxt
        self.rotateBtn.clicked.connect(self.rotate)

        
        #clutch
        self.clutchBtn=self.ui.clutchBtn
        self.clutchBtn.setEnabled(False)

        self.clutchBtn.setText("Gear")
        
        self.clutchBtn.clicked.connect(self.engageClutch)

        #finish
        self.finishPrimeBtn=self.ui.finishPrimeBtn
        self.finishPrimeBtn.clicked.connect(self.stopPriming)


    def enablePriming(self):
        self.rotateBtn.setEnabled(True)
        self.clutchBtn.setEnabled(True)
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
            
        else:
            self.clutchBtn.setText("Gear")
            self.clutch=False
        
        self.updateStatus()
            

    def stopPriming(self):
        self.ui.tabWidget.setCurrentIndex((self.ui.tabWidget.currentIndex()+1))

        pass
