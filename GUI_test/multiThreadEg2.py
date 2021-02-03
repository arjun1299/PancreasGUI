import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from queue import Queue


import time
import sys
import logging


global LOG
LOG=False


class Logger(QThread):
    
    q=Queue()

    def run(self):
        
        while 1:
            if self.q.empty()==False :
                s= Logger.q.get()
                if s=="Stop":
                    break
                print("Logged!"+ s )
                logging.info(s)

            time.sleep(0.1)


class Worker(QThread):
    progress=pyqtSignal(str)
    

    def __init__(self,*args):
        super().__init__()
        self.args=args
        


    def complete(self):
        print("Thread finished")

    def run(self):
        #self.setPriority(QThread.HighestPriority)
        _=0

        while _<10:

            #1000000
            print(f"Thread with {self.args} running: {_}")
            if LOG:
                self.progress.emit(str(self.args)+" Finished executing "+str(_))
            _+=1

            time.sleep(1)





class MainWindow(QMainWindow):
    
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUI()
        self.cnt1=0
        self.cnt2=0

        self.logger=Logger()

    def setupUI(self):
        """
        Thread switching interval can be set from here
        """

        #sys.setswitchinterval(0.05)
        print(sys.getswitchinterval())

        self.btn1=QPushButton('Button1',self)
        self.btn2=QPushButton('Button2',self)
        self.btn3=QPushButton('Start log',self)
        self.btn4=QPushButton('Stop log',self)
        
        self.resize(300,100)
        self.btn2.move(0,60)
        self.btn3.move(120,60)
        self.btn4.move(120,0)

        #inline function used
        self.btn1.clicked.connect(lambda v: self.execute1("1"))
        self.btn2.clicked.connect(lambda v: self.execute2("2"))
        self.btn3.clicked.connect(self.startLog)
        self.btn4.clicked.connect(self.stopLog)
        

        logging.basicConfig(filename="log.txt",format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)
        logging.warning("Started")

    def execute1(self,args):
        #This is the thread count of this instance
        self.cnt1+=1


        self.worker1=Worker(args,self.cnt1)
        self.worker1.finished.connect(self.finished1 )

        self.worker1.progress.connect(self.addToQueue )
        #self.worker1.setPriority(QThread.HighestPriority)
   
        self.worker1.start()

    def finished1(self):
        #decrement instance count
        self.cnt1=self.cnt1-1

    def execute2(self,args):
        self.cnt2+=1
        self.worker2=Worker(args,self.cnt2)
        self.worker2.start()
        self.worker2.finished.connect(self.finished2 )
        self.worker2.progress.connect(self.addToQueue )

    def finished2(self):
        self.cnt2=self.cnt2-1
    

    def startLog(self):
        global LOG
        LOG=True
        self.logThread=Logger()
        
        self.logThread.start()
        
    
    def stopLog(self):
        global LOG
        LOG=False
        logging.warning("---Stopped logging---")
        Logger.q.put("Stop")

    def addToQueue(self,arg):
        Logger.q.put(arg)

app=QApplication(sys.argv)
window=MainWindow()
window.show()
e=app.exec()
logging.warning("________CLOSED________")
sys.exit(e)