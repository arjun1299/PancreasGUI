import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from queue import Queue


import time
import sys
import logging


LOG=True

class Logger(QThread):

    q=Queue()

    def __init__(self):
        super().__init__()

        #logger config
        logging.basicConfig(filename="logButton.txt",format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)
        logging.warning("Started")

    def run(self):
        while 1:
            if self.q.empty()== False:
                s= Logger.q.get()
                logging.info(s)
            time.sleep(0.1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.btn1=QPushButton('Reset Time',self)
        self.btn1.clicked.connect(self.resetTimer)
        self.timer= QTimer()
        self.timer.timeout.connect(self.timeoutEvent)
        self.timer.start(2000)

        self.btn2 =QPushButton('Stop time',self)
        self.btn2.clicked.connect(self.stopTimer)
        self.btn2.move(0,60)

        self.loggingModule=Logger()
        self.loggingModule.start()


    def stopTimer(self):

        Logger.q.put("Stopped timer")
        self.timer.stop()
        self.btn1.setText("Start timer")


    def timeoutEvent(self):
        Logger.q.put("ERROR: Timeout")
        print("Error")
        
        while Logger.q.empty()==False:
            time.sleep(0.1)
        sys.exit()

    def resetTimer(self):
        self.btn1.setText("Reset timer")
        self.timer.stop()
        self.timer.start(2000)
        Logger.q.put("Reset Timer")

app=QApplication(sys.argv)
window=MainWindow()
window.show()
e=app.exec()
sys.exit(e)