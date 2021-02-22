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

    engageClutch=pyqtSignal()
    insulonComplete=pyqtSignal(str)
    logicSendHeartBeat=pyqtSignal()
    
    sendHeartBeat=pyqtSignal()
    timeoutSignal=pyqtSignal()
    
    heartbeatTimeoutTime=10000
    heartbeatPeriod=5000
    heartBeatFailFlag=False




    def __init__(self,*args):
        super().__init__()
        self.args=args

        """Heart beat checker variables
        """


        
        self.heartBeatSenderTimer=QTimer() #connect this to hbSend
        self.heartBeatRecieverTimer=QTimer()#this needs to be connected to a timeout event
        self.heartBeatSenderTimer.timeout.connect(self.hbSend)

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

                """
                Sender success cases
                """
                if(data[:3]=="SSS"):
                    if(data[3:]=="LHB"):
                        if self.heartBeatFailFlag==True:
                            pass
                        else:
                            self.hbRecieverTimerReset.emit()

                if(data=="LHB"):
                    self.logicSendHeartBeat.emit()

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
    
    def postSendFunctions(self,data):
        self.pq.put((1,"SSS"+data))

    
    def hbSend(self):
        """
        Sends the heartbeat repeatedly
        """
        self.sendHeartBeat.emit()
        
        self.heartBeatSenderTimer.start(Logic.heartbeatPeriod)
    
    def heartBeatTimeout(self):
        """
        Timeout function if hearbeat is not recieved in time
        """
        self.logic.heartBeatFailFlag=True
        Logger.q.put("ERROR","Heartbeat Timeout!!")
