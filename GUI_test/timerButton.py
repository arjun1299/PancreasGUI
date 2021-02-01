import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from queue import Queue


import time
import sys
import logging


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.btn1=QPushButton('Button1',self)
        self.btn1.clicked.connect(self.resetTimer)
        self.timer= QTimer()
        self.timer.timeout.connect(self.timeoutEvent)
        self.timer.start(1000)
    def timeoutEvent(self):
        print("Error")
        sys.exit()
    def resetTimer(self):
        self.timer.stop()
        self.timer.start(2000)

app=QApplication(sys.argv)
window=MainWindow()
window.show()
e=app.exec()
sys.exit(e)