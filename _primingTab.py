
"""
Tab-2
Priming
"""

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtTest import QTest

from loggingModule import *

class primingTab(object):
    def init_primingTab(self):
        #start prime
        self.startPrimeBtn=self.ui.startPrimeBtn
        self.startPrimeBtn.setEnabled(True)
        
        #Try except block used to disconnect old connections if reset occours, else the same function gets executed twice
        try:
            self.startPrimeBtn.clicked.disconnect()
        except:
            pass
        self.startPrimeBtn.clicked.connect(self.enablePriming)
        
    
        #rotate
        self.rotateBtn=self.ui.rotateBtn
        self.rotateBtn.setEnabled(False)
        self.countTxt=self.ui.countTxt
        #Try except block used to disconnect old connections if reset occours, else the same function gets executed twice
        try:
            self.rotateBtn.clicked.disconnect()
        except:
            pass
        self.rotateBtn.clicked.connect(self.rotate)

        
        #clutch
        self.toggleClutchBtn=self.ui.toggleClutchBtn
        self.toggleClutchBtn.setEnabled(False)

        try:
            self.toggleClutchBtn.clicked.disconnect()
        except:
            pass
        self.toggleClutchBtn.clicked.connect(self.engageClutch)

        #fixed prime
        self.fixedPrimeBtn=self.ui.fixedPrimeBtn
        self.primingBar=self.ui.primingBar
        self.primingBar.setVisible(False)
        #Try except block used to disconnect old connections if reset occours, else the same function gets executed twice
        try:
            self.fixedPrimeBtn.clicked.disconnect()
        except:
            pass
        self.fixedPrimeBtn.clicked.connect(self.fixedPrime)
        self.fixedPrimeBtn.setEnabled(False)

        #finish
        self.finishPrimeBtn=self.ui.finishPrimeBtn
        #Try except block used to disconnect old connections if reset occours, else the same function gets executed twice
        try:
            self.finishPrimeBtn.clicked.disconnect()
        except:
            pass
        self.finishPrimeBtn.clicked.connect(self.finishPriming)
        self.finishPrimeBtn.setEnabled(False)

        #reset
        self.resetBtn=self.ui.resetBtn
        try:
            self.resetBtn.clicked.disconnect()
        except:
            pass
        self.resetBtn.clicked.connect(self.resetActuation)

        self.stopPriming=False
        self.primingRotations=0


    def enablePriming(self):
        Logger.q.put(("WARNING","Starting priming"))
        self.rotateBtn.setEnabled(True)
        self.toggleClutchBtn.setEnabled(True)
        #self.fixedPrimeBtn.setEnabled(True)
        self.ongoing="Priming"
        #self.showDialog("Prime")
        self.updateStatus()
        
        #default clutch pos
        self.toggleClutchBtn.setText("Ratchet")
        self.clutch=True
        self.logic.pq.put((1,"SPC"))
        Logger.q.put(("INFO","Switching to Gear"))

    def rotate(self):
        #do rotations, manual prime
        self.resetBtn.setEnabled(False)
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
        else:
            num=0
        if num!=0:
            self.showWarning("Rotations complete!")
        self.resetBtn.setEnabled(True)

            

    def engageClutch(self):
        #True is gear side
        #False is ratchet

        self.fixedPrimeBtn.setEnabled(True)
        if self.clutch== False:
            self.toggleClutchBtn.setText("Ratchet")
            self.clutch=True
            self.logic.pq.put((1,"SPC"))
            Logger.q.put(("INFO","Switching to Ratchet"))
            
        else:
            self.toggleClutchBtn.setText("Gear")
            self.clutch=False
            self.logic.pq.put((1,"SDC"))
            Logger.q.put(("INFO","Switching to Gear"))
        
        self.updateStatus()
            

    def finishPriming(self):
        self.ui.tabWidget.setCurrentIndex(2)
        #Making sure it is on the delivery chain side
        self.logic.pq.put((1,"SDC"))
        self.startPrimeBtn.setEnabled(False)
        self.rotateBtn.setEnabled(False)
        self.toggleClutchBtn.setEnabled(False)
        self.fixedPrimeBtn.setEnabled(False)
        self.ui.tabWidget.setTabEnabled(2,True)

    def fixedPrime(self):
        self.resetBtn.setEnabled(False)
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
                self.primingBar.setVisible(True)
                self.primingBar.setValue(float(i)/insulons*100)
                self.logic.pq.put((1,"SIN"))
                QTest.qWait(1500)
        
        
        
        

        if insulons!=0:
            self.primingBar.setValue(100)
            self.showWarning("Fixed prime complete!")
            self.primingBar.setVisible(False)
            self.finishPrimeBtn.setEnabled(True)
        self.resetBtn.setEnabled(True)

