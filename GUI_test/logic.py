from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from untitled import Ui_MainWindow

from bleOperations import *
from logicModule import *
from multithread import *

import time
import traceback, sys
import os




class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.threadpool=QThreadPool()

        self.threadHandle(self.looper)
        #self.ui.pushButton.clicked.connect(self.loopHandle)
        self.ui.pushButton.clicked.connect(lambda v: self.threadHandle(self.looper))
        self.ui.pushButton_2.clicked.connect(lambda v: self.threadHandle(self.scan))
        """
        Start serial listener and connect it to parser queue

        """
        
        self.serialListner =SerialListner()
        self.serialListner.dataArrival.connect(self.addToParserQueue)
        self.serialListner.start()
        

        """
        Timer for heartbeat
        """

        self.heartBeatTimer=QTimer()
        self.timeout.connect(self.heartBeatTimeout)
        
        """
        Section to start parser
        """
        self.parser=Parser()
        self.parser.addToLogicQueue.connect(self.addToLogicQueue)
        self.parser.start()       

        """
        Start sender
        """ 
        self.sender=Sender()
        self.sender.sendData.connect(self.sendData)
        self.sender.start()   

        """
        Section to Logic
        """
        self.logic=Logic()
        ###Connect all logic signals
        self.logic.hbTimerReset.connect(self.hbTimerReset)
        self.logic.start()   

        """
        Check if ble is connected
        """

        worker=Worker(self.isConnectedBLE)
        worker.signals.finished.connect(self.finish)
        print("Starting hb")
        self.threadpool.start(worker)



    def scanHandle(self):
        """Starts the scanning thread
        """
        worker=Worker(self.scan)
        self.threadpool.start(worker)

    def threadHandle(self,fun):
        """
        A generic thread starting function
        
        :param fun: A function which needs to run in a threadpool
        :type fun: Function
        """
        worker=Worker(fun)
        worker.signals.finished.connect(self.finished)
        self.threadpool.start(worker)
                
    def finished(self):
        print("Done!!!!!!!!!!!!!")

    def addToLogicQueue(self,args):
        """Adds argument to logic queue for processing
        :param args: A string which is used by the logic module if-else ladder
        :type args: String
        """
        Logic.put(args)

    def hbTimerReset(self):
        """
        Resets the heartbeat timer
        """
        self.heartBeatTimer.stop()
        self.heartBeatTimer.start(2000)


    def heartBeatTimeout(self):
        """
        Timeout function if hearbeat is not recieved in time
        """

        self.showError("Heart beat missing")
        self.init_connectTab()
        self.showError("Device disconnected")
        self.bleConnectionStatus="Disconnected"
        self.updateStatus()
        
        self.ui.tabWidget.setCurrentIndex(0)
        self.disconnectBtn.setEnabled(False)
        self.uart_connection.disconnect()

    def sendData(self,data):
        """Function to send data via the Bluetooth adapter to the BLE module on the device

        :param data: A stromg which needs to be sent over ble
        :type data: String
        """
        if self.uart_service:
            self.uart_service.write(data.encode("utf-8"))
            print("Sent: "+data)


    def sendHB(self):
        """
        Send a Heart Beat signal to the BLE module
        """
        if(self.uart_service):
            self.heartBeatTimer.start(2000) #starting heartbeat timer
            print("HB sent")
            s="IPHB\r"
            print("Sent HB")
            self.sender.q.put(s)
        else:
            print("Cant send HB, no uart")


    def isConnectedBLE(self):
        """
        Checks if the BLE module is still connected to the device
        """
        #check for ble connection here
        print("Starting HB")
        while 1:
            if self.uart_service:
                if self.uart_connection.connected:
                    self.sendHB()
                else:
                    self.uart_service=False
            time.sleep(0.1)

    def addToParserQueue(self):
        """This function is used by the listener to keep adding data into the parser queue 
        """
        if(self.uart_service):
            if(self.uart_service.in_waiting):
                raw_serial=self.uart_service.readline()
                if raw_serial:
                    Parser.q.put(raw_serial)
                    print("Added to parser queue")

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
