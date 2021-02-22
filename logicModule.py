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

    hbRecieverTimerReset=pyqtSignal()
    hbSenderTimerReset=pyqtSignal()
    sendHB=pyqtSignal()
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
                if(data[0:2]=="SS"):
                    if(data[2:]=="SHB"):
                        self.hbRecieverTimerReset.emit()


                """
                Sender functions
                """
                """
                Incoming from BLE
                """
                if(data[:2]=="HB"):
                    print("Emitting hb Reset")
                    self.hbSenderTimerReset.emit()

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

class heartBeatChecker(QTimer):
    """This class contains all timers required for the funtioning of the heartbeat

    :param QTimer: [description]
    :type QTimer: [type]
    """

    heartBeatSenderInterval=2000
    heartBeatRecieverInterval=7000

    sendHeartBeat=pyqtSignal()
    timeoutSignal=pyqtSignal()

    
    def __init__(self):
        """
        Timer for heartbeat

        """
        super().__init__()
        self.q=Queue()

        self.heartBeatFlag=False
        self.heartBeatSenderTimer = QTimer() #connect this to hbSend
        self.heartBeatRecieverTimer = QTimer()#this needs to be connected to a timeout event
        self.heartBeatSenderTimer.timeout.connect(self.hbSend)


    def hbRecieverTimerReset(self):
        """
        Resets the heartbeat timer
        """
        print("Reset reciever heartbeat timer")

        self.heartBeatSenderTimer.stop()
        self.heartBeatRecieverTimer.stop()
        self.heartBeatRecieverTimer.start(heartBeatChecker.heartBeatRecieverInterval)

    def hbSenderTimerReset(self):
        """Sender heart beat timer reset
        """

        self.heartBeatSenderTimer.stop()
        self.heartBeatRecieverTimer.stop()
        self.heartBeatSenderTimer.start(heartBeatChecker.heartBeatSenderInterval)

    
    def hbSend(self):
        """
        Sends the heartbeat repeatedly
        """
        self.sendHeartBeat.emit()
        self.heartBeatSenderTimer.start(2000)

        