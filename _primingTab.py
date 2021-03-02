
"""
Tab-2
Priming
"""

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from loggingModule import *

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
        self.fixedPrimeBtn.clicked.connect(self.fixedPrime)
        self.fixedPrimeBtn.setEnabled(False)

        #finish
        self.finishPrimeBtn=self.ui.finishPrimeBtn
        self.finishPrimeBtn.clicked.connect(self.stopPriming)


    def enablePriming(self):
        Logger.q.put(("WARNING","Starting priming"))
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
        self.logic.pq.put((1,"SIN"))
        self.countTxt.setText(str(self.primingRotations))
        

    def engageClutch(self):
        if self.clutch== False:
            self.toggleClutchBtn.setText("Ratchet")
            self.clutch=True
            self.logic.pq.put((1,"SDC"))
            Logger.q.put(("INFO","Switching to Ratchet"))
            
        else:
            self.toggleClutchBtn.setText("Gear")
            self.clutch=False
            self.logic.pq.put((1,"SPC"))
            Logger.q.put(("INFO","Switching to Gear"))
        
        self.updateStatus()
            

    def stopPriming(self):
        self.ui.tabWidget.setCurrentIndex((self.ui.tabWidget.currentIndex()+1))

        pass

    def fixedPrime(self):
        for i in range(2):
            self.logic.pq.put((1,"SIN"))
            time.sleep(0.1)

        pass
