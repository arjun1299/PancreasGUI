import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from queue import Queue
from logicModule import Logic

import time
import sys
import logging

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

TIMEOUT=1
connected_to_device=False

class Parser(QThread):
    q=Queue()

    addToLogicQueue=pyqtSignal(tuple)

    def __init__(self,*args):
        super().__init__()
        self.args=args
        print("Parser started")

    def run(self):
        while 1:
            #print("Thread recieved")
            #print("Running parser")
            if(self.q.empty()==False):
                data=self.q.get().decode("utf-8")
                
                self.addToLogicQueue.emit((1,data))

                print("Parsed:"+data)
            time.sleep(0.1)

class SerialListner(QThread):
    """Listens to the buffer and loads any sends signals to load any incoming data to serial

    :param QThread: [description]
    :type QThread: [type]
    """
    dataArrival=pyqtSignal()

    def __init__(self):
        super().__init__()
        self.target= "F9:9B:81:05:DE:E7"
        print("Listener started")
    
    def run(self):
        while 1:
            self.dataArrival.emit()
            #This function needs to keep running and check the uart buffer if any charachters are incoming
            time.sleep(0.1)

class Sender(QThread):
    """
    The sender class is what manages the sending instructions to the device

    :param QThread: [description]
    :type QThread: [type]
    """

    
    sendData=pyqtSignal(str)

    def __init__(self,*args):
        super().__init__()
        self.args=args
        self.q=Queue()
        print("Sender started")


    def run(self):
        while 1:
            if(self.q.empty()==False):
                self.sendData.emit(self.q.get())
        time.sleep(0.1)

    def sendHB(self):
        """
        Send a Heart Beat signal to the BLE module
        """
        s="IPHB\r"
        print("Sent HB")
        self.q.put(s)
        print("Cant send HB, no uart")


class connectionChecker(QTimer):

    sendHeartBeat=pyqtSignal()
    timeoutSignal=pyqtSignal()

    
    def __init__(self):
        """
        Timer for heartbeat

        """
        super().__init__()
        self.q=Queue()

        self.heartBeatFlag=False
        self.heartBeatSenderTimer=QTimer() #connect this to hbSend
        self.heartBeatRecieverTimer=QTimer()#this needs to be connected to a timeout event
        self.heartBeatSenderTimer.timeout.connect(self.hbSend)

    def hbTimerReset(self):
        """
        Resets the heartbeat timer
        """
        print("Reset heartbeat timer")
        self.heartBeatRecieverTimer.stop()
        self.heartBeatRecieverTimer.start(5000)
    
    def hbSend(self):
        """
        Sends the heartbeat repeatedly
        """
        self.sendHeartBeat.emit()
        
        self.heartBeatSenderTimer.start(2000)
    