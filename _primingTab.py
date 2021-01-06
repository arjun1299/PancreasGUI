
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



    def enablePriming(self):
        self.rotateBtn.setEnabled(True)
        self.stopBtn.setEnabled(True)
        self.ongoing="Priming"
        self.showDialog("Prime")
        self.updateStatus()

    def rotate(self):
        #do one rotation
        pass


    def stopPriming(self):
        #do one rotation
        pass
