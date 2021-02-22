import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from queue import Queue
from logicModule import Logic

import time
import sys
from loggingModule import *

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

TIMEOUT=1
connected_to_device=False

class Parser(QThread):
    """
    This module parses the incoming data
    :param QThread: [description]
    :type QThread: [type]
    """
    q=Queue()
    addToLogicQueue=pyqtSignal(tuple)

    def __init__(self,*args):
        super().__init__()
        self.args=args
        print("Parser started")

    def run(self):
        Logger.q.put(("INFO","Parser Thread Started successfully"))

        while 1:
            #print("Thread recieved")
            #print("Running parser")
            """Changed from if to while
            """
            while(self.q.empty()==False):
                data=self.q.get()

                if data=="Stop":
                    break

                data=data.decode("utf-8")
                
                self.addToLogicQueue.emit((1,data))

                print("Parsed:"+data)
                Logger.q.put(("INFO","Parsed:"+data))

            time.sleep(0.1)

class SerialListner(QThread):
    """Listens to the buffer and loads any sends signals to load any incoming data to serial

    :param QThread: [description]
    :type QThread: [type]
    """
    checkDataArrival=pyqtSignal()
    SerialListnerEnable=True

    def __init__(self):
        super().__init__()
        self.target= "F9:9B:81:05:DE:E7"
        
        SerialListner.SerialListnerEnable=True
    
    def run(self):
        """
        This function needs to keep running and check the uart buffer if any charachters are incoming
        """
        print("Listener Started")

        Logger.q.put(("INFO","Serial Listner Thread started"))

        while 1:

            if SerialListner.SerialListnerEnable==False:
                break

            self.checkDataArrival.emit()
            
            time.sleep(0.1)

class Sender(QThread):
    """
    The sender class is what manages the sending instructions to the device

    :param QThread: [description]
    :type QThread: [type]
    """

    sendSuccess=pyqtSignal(str)
    sendData=pyqtSignal(str)
    q=Queue()

    def __init__(self,*args):
        super().__init__()
        self.args=args
        

    def run(self):
        print("Sender started")

        while 1:
            if(self.q.empty()==False):
                data=self.q.get()

                if data=="Stop":
                    break
                
                self.sendData.emit(data)
            time.sleep(0.1)

    def sendHB(self):
        """
        Send a Heart Beat signal to the BLE module
        """

        s="IPHB\r"
        print("Sent HB")
        self.q.put(s)




    