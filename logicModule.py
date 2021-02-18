import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from queue import Queue,PriorityQueue

from loggingModule import *

import time
import sys
import logging


class Logic(QThread):
    pq=PriorityQueue()

    hbTimerReset=pyqtSignal()
    engageClutch=pyqtSignal()
    insulonComplete=pyqtSignal(str)


    def __init__(self,*args):
        super().__init__()
        self.args=args

        """Flag indicates that the next incoming value is the inulon time
        """
        self.insulonCompleteFlag=False

    def run(self):
        while 1:
            #print("Thread recieved")
            #print("Running parser")
            if(self.pq.empty()==False):#if there is any value
                #the first element is the priority
                data=self.pq.get()[1]
                print("Logic:"+data)
                Logger.q.put(("INFO","Logic queue recieved: "+ data))
                if(data=="Stop"):
                    break
                """
                    Start switch case statement
                """

                    

                if(data[:2]=="HB"):
                    print("Emitting hb Reset")
                    self.hbTimerReset.emit()

                elif(self.insulonCompleteFlag):
                    print(data)
                    self.insulonCompleteFlag=False
                    self.insulonComplete.emit(data) 

                elif(data[:2]=="IN"):
                    """
                    Data comes in as
                    INXX.XX where X is the time taken for one insulon rotation
                    """
                    print("Emitting IN")
                    self.insulonComplete.emit(data[2:]) 
               
                
            time.sleep(0.1)
