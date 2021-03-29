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
    """This is a priority queue which deals with logic, stop commands typically have highest priority and the reset of the comands are equal
    """

    hbRecieverTimerReset=pyqtSignal()
    """Executed on a timer which needs to be stopped
    """
    hbSenderTimerReset=pyqtSignal()
    """heartbeat sender timer reset is connected to this signal
    """
    hbStop=pyqtSignal()
    """heartbeat stop is connected
    """
    sendHB=pyqtSignal()
    """Signal adds a HB to the sender queue
    """
    sendIN=pyqtSignal()
    """Signal to send an insulon
    """
    sentIN=pyqtSignal()
    sendPC=pyqtSignal()
    """Send a priming chain command
    """
    sendDC=pyqtSignal()
    """Send a delivery chain command
    """
    sendUN=pyqtSignal()
    """Send a reverse rotation command
    """

    #Error signals
    actuationLimitReached=pyqtSignal()
    """If actuation limit is reached this signal is called
    """
    stopActuation=pyqtSignal()
    """If a stop signal is detected this signal is emitted in order to stop all actuation
    """
    ratchetSlipOccoured=pyqtSignal()
    """If a ratchet slip is detected this signal is raised
    """
    

    engageClutch=pyqtSignal()
    """This signal is used for clutch engagement functions
    """
    insulonComplete=pyqtSignal(str)
    """On insulon complete, this signal send the encoder value back
    """
    updateActuationLength=pyqtSignal()
    """Signal to update the actuation length after every movement
    """

    def __init__(self,*args):
        super().__init__()
        self.args=args

        """Flag indicates that the next incoming value is the inulon time
        """
        self.sendInsulonFlag=False
        
        #This is a safety feature to take care of over actuation
        self.allowActuation=True

        self.prevEncoderValue=0
        self.currentEncoderValue=0

    def run(self):
        """
        Branching out of logic happens in this function, all instructions and processes pass through this and appropriate signals are raised
        """
        while 1:
            #print("Thread recieved")
            #print("Running parser")
            while(self.pq.empty()==False):#if there is any value
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
                    elif(data[2:]=="SIN"):
                        self.sentIN.emit()
                
                    """
                    Sender functions
                    """
                elif(data=="SIN"):
                    #send insulon
                    if self.allowActuation==True:
                        self.sendIN.emit()
                        self.updateActuationLength.emit()
                    else:
                        #self.actuationLimitReached.emit()
                        self.stopActuation.emit()
                elif(data=="SUN"):
                        self.sendUN.emit()

                elif(data=="SHB"):
                    #send heartbeat
                    self.sendInsulonFlag=False
                    self.sendHB.emit()
                elif(data=="INSHB"):
                    #send heartbeat before insulon
                    self.sendInsulonFlag=True
                    self.sendHB.emit()
                elif(data=="SPC"):
                    self.sendPC.emit()
                elif(data=="SDC"):
                    self.sendDC.emit()

                    """
                    Incoming from BLE
                    """
                elif(data[:2]=="HB"):
                    
                    #if the hb was returned and the next step is to send an insulon
                    if(self.sendInsulonFlag==True):
                        self.pq.put((1,"SIN"))
                        self.sendInsulonFlag=False
                        self.hbStop.emit()
                    else:
                        print("Emitting hb Reset")
                        self.hbSenderTimerReset.emit()
                        
                elif(data[:2]=="IN"):
                    """
                    Data comes in as
                    INXX.XX where X is the time taken for one insulon rotation
                    """
                    print("Emitting IN")
                    self.insulonComplete.emit(data[2:])
                    
                    #Handling encoder data
                    
                    #Ratchet slip condition
                    self.currentEncoderValue=data[2:]
                    if(self.prevEncoderValue==self.currentEncoderValue):
                        self.ratchetSlipOccoured.emit()
                    self.prevEncoderValue=self.currentEncoderValue
                    self.currentEncoderValue=data[2:]
                    
                elif(data=="DC"):
                    print("Switched to delivery chain")
                elif(data=="PC"):
                    print("Switched to priming chain")
                elif(data=="STOP"):
                    self.stopActuation.emit()
                    
            time.sleep(0.0005)

    def addHBLogic(self):
        """Add sender heartbeat into the logic queue
        """
        self.pq.put((1,"SHB"))

    def heartBeatSent(self):
        self.pq.put((1,"SSSHB"))
    def insulonSent(self):
        self.pq.put((1,"SSSIN"))

class heartBeatChecker(QTimer):
    """This class contains all timers required for the funtioning of the heartbeat, the timers should run on the main thread

    :param QTimer: [description]
    :type QTimer: [type]
    """

    heartBeatSenderInterval=2000
    heartBeatRecieverInterval=3000

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

    def hbStop(self):
        """Stops heartbeat timers
        """
        self.heartBeatSenderTimer.stop()
        self.heartBeatRecieverTimer.stop()
    

    
    def hbSend(self):
        """
        Sends the heartbeat repeatedly
        """
        self.sendHeartBeat.emit()
        #self.heartBeatSenderTimer.start(2000)

        