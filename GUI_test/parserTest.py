import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from queue import Queue

import time
import sys
import logging

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

TIMEOUT=1
connected_to_device=False

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


class Parser(QThread):
    q=Queue()

    def __init__(self,*args):
        super().__init__()
        self.args=args

    def run(self):
        while 1:
            #print("Thread recieved")
            #print("Running parser")
            if(Parser.q.empty()==False):
                print("Parsed:"+Parser.q.get().decode("utf-8"))
            time.sleep(0.1)

class SerialListner(QThread):
    dataArrival=pyqtSignal()

    def __init__(self):
        super().__init__()
        self.target= "F9:9B:81:05:DE:E7"
    
    def run(self):
        while 1:
            #print("Running listener")
            self.dataArrival.emit()
            time.sleep(0.1)
    
    def assignUART(args):
        self.uart_connection=args

class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUI()
        
    def setupUI(self):
        self.btn1=QPushButton('Button1',self)
        self.btn1.clicked.connect(self.connectToBLE)

        self.btn2= QPushButton('Button2',self)
        self.btn2.move(0,60)
        self.btn2.clicked.connect(self.sendHB)

        self.serialListner =SerialListner()
        #self.serialListner.started.connect(self.serialListner.assignUART)
        self.serialListner.dataArrival.connect(self.addToParserQueue)
        self.serialListner.start()
        self.uart_service=0
        

        self.parser=Parser()
        self.parser.start()
        
        self.sender=Sender()
        self.sender.sendData.connect(self.sendData)
        self.sender.start()
        
    def sendData(self,data):
        """Function to send data via the Bluetooth adapter to the BLE module on the device

        :param data: A stromg which needs to be sent over ble
        :type data: String
        """
        if self.uart_service:
            self.uart_service.write(data.encode("utf-8"))
            print("Sent: "+data)
        

    def connectToBLE(self):
    
        ble = BLERadio()
 
        uart_connection = None
        
        while not uart_connection:
            print("Trying to connect...")
            #for adv in ble.start_scan(ProvideServicesAdvertisement):
            for adv in ble.start_scan(ProvideServicesAdvertisement):        
                print(adv)
                if UARTService in adv.services:
                    uart_connection = ble.connect(adv)
                    print("Connected")
                    break
            ble.stop_scan()
        self.uart_service=uart_connection[UARTService]
        
        if self.uart_service:
          print("Connection sequence complete")

    def sendHB(self):
        """
        Send a Heart Beat signal to the BLE module
        """
        if(self.uart_service):
            s="IPHB\r"
            #print("Sent HB")
            self.sender.q.put(s)
        else:
            print("Cant send HB, no uart")
        
        

    
    
    def addToParserQueue(self):
        if(self.uart_service):
            while(self.uart_service.in_waiting):
                print(self.uart_service.in_waiting)
                raw_serial=self.uart_service.readline()
                #self.uart_service.reset_input_buffer()
                if raw_serial:
                    Parser.q.put(raw_serial)
                    print("Added to parser queue")


app=QApplication(sys.argv)
window=MainWindow()
window.show()
e=app.exec()
sys.exit(e)
