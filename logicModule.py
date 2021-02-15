import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from queue import Queue,PriorityQueue


import time
import sys
import logging


class Logic(QThread):
    pq=PriorityQueue()

    hbTimerReset=pyqtSignal()
    engageClutch=pyqtSignal()


    def __init__(self,*args):
        super().__init__()
        self.args=args

    def run(self):
        while 1:
            #print("Thread recieved")
            #print("Running parser")
            if(self.pq.empty()==False):#if there is any value
                #the first element is the priority
                data=self.pq.get()[1]
                print("Logic:"+data)
                """
                    Start switch case statement
                """
                if(data[:2]=="HB"):
                    print("Emitting hb Reset")
                    self.hbTimerReset.emit()
            time.sleep(0.1)
