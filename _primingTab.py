
"""
Tab-2
Priming
"""

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtTest import QTest

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
        self.finishPrimeBtn.clicked.connect(self.finishPriming)

        #reset
        self.resetBtn=self.ui.resetBtn
        self.resetBtn.clicked.connect(self.resetActuation)

        self.stopPriming=False


    def enablePriming(self):
        Logger.q.put(("WARNING","Starting priming"))
        self.rotateBtn.setEnabled(True)
        self.toggleClutchBtn.setEnabled(True)
        #self.fixedPrimeBtn.setEnabled(True)
        self.ongoing="Priming"
        #self.showDialog("Prime")
        self.updateStatus()
        
        #default clutch pos
        self.clutch=False
        self.logic.pq.put((1,"SPC"))
        self.toggleClutchBtn.setText("Gear")
        Logger.q.put(("INFO","Switching to Gear"))

    def rotate(self):
        #do one rotation
        num, ok = QInputDialog.getText(self, 'Number of rotations', 'Number:')
        
        delayTimer=QTimer()

        if num.isnumeric():
            num=int(num)

            for i in range(num):
                if self.stopPriming==False:
                    self.primingRotations+=1
                    
                    #self.countTxt.setFontPointSize(20)
                    self.logic.pq.put((1,"SIN"))
                    self.countTxt.setText(str(self.primingRotations))
                    QTest.qWait(1500)

            

    def engageClutch(self):

        self.fixedPrimeBtn.setEnabled(True)
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
            

    def finishPriming(self):
        self.ui.tabWidget.setCurrentIndex((self.ui.tabWidget.currentIndex()+1))

        pass

    def fixedPrime(self):

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Fixed Prime")
        msgBox.setWindowTitle("Message")
        fixed_6IU=msgBox.addButton("0.6 IU",QMessageBox.YesRole)
        fixed_9IU=msgBox.addButton("0.9 IU",QMessageBox.YesRole)
        msgBox.addButton(QMessageBox.No)
        
        returnValue = msgBox.exec_()
        print("*********",returnValue)
        insulons=0

        #it returns 0,1,2.. based on the button pressed
        if returnValue==0:
            Logger.q.put(("INFO","0.6 IU Fixed Prime"))
            insulons=12

        elif returnValue==1:
            Logger.q.put(("INFO","0.9 IU Fixed Prime"))
            insulons=18
        
        for i in range(insulons):
            if self.stopPriming==False:
                self.logic.pq.put((1,"SIN"))
                QTest.qWait(1500)

