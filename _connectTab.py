import os
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout, QProgressBar, QVBoxLayout,QLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QMovie

from multithread import Worker,WorkerSignals


from adafruit_ble import BLERadio

from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService


"""
    Tab 1- connect tab
"""
    
class connectTab(object):


    def init_connectTab(self):
        #self.check=self.ui.checkBox
        self.chk()
        #self.check.clicked.connect(self.chk)
        #dropdown

        
        
        self.dropdown=self.ui.comboBox
        #scan button
        self.scanButton=self.ui.scanButton
        self.scanButton.clicked.connect(self.scanPort)
        #connect button
        self.connectButton=self.ui.connectButton
        self.connectButton.setEnabled(False)
        self.connectButton.clicked.connect(self.connectPort)

        self.disconnectBtn.setEnabled(False)

        self.scanLbl=self.ui.scanLbl
        
        
        self.movie = QMovie("loader.gif")
        self.scanLbl.setMovie(self.movie)        
        
        #check availability of bluetooth functionality
        while(self.isConnectedReciever()==0):
            self.connectButton.setEnabled(False)
            self.scanButton.setEnabled(False)
        self.scanButton.setEnabled(True)
        

    def isConnectedBLE(self):
        #check for ble connection here
        print("Starting HB")
        while self.uart_connection.connected:
                uart_service=self.uart_connection[UARTService]
                s = "IPHB"
                print("HB sent")
                uart_service.write(s.encode("utf-8"))
                uart_service.write(b'\r')
                r= uart_service.readline().decode("utf-8")
                uart_service.readline().decode("utf-8")
                print(r)
                if("HB" not in r ):
                    self.init_connectTab()
                    self.showError("Device disconnected")
                    self.bleConnectionStatus="Disconnected"
                    self.updateStatus()
                    
                    self.ui.tabWidget.setCurrentIndex(0)
                    self.disconnectBtn.setEnabled(False)
                    self.uart_connection.disconnect()
                    
                    #exit()
                    break


    def isHeartBeat(self):

        pass

    def isConnectedReciever(self):
        #checks if bluetooth reciever is connected
        if(os.system("timeout -s INT 1s hcitool lescan")== 256):
            #print("BLUETOOTH ADAPTER NOT FOUND")
            self.showError("BLUETOOTH ADAPTER NOT FOUND")
            exit()
            #return 0
        return 1


    def chk(self):
        #enable tabs
        #se lf.ui.tabWidget.setTabEnabled(1,self.isConnectedBLE())
        #self.ui.tabWidget.setTabEnabled(2,self.isConnectedBLE())
        pass


    def connectPort(self):
        if(self.dropdown.currentText()):
            self.port=self.dropdown.currentText()
            ble=BLERadio()
            
            """
            #add logic to pair with BLE
            """

            print("Connected to:"+self.dropdown.currentText())
            for element in self.comlist:
                if element.complete_name ==  self.dropdown.currentText() or self.dropdown.currentText() in str(element.address):
                        #no check if uart service works
                        
                        try:
                            if(UARTService in element.services or self.targetAddress in str(element.address)):
                                self.uart_connection = ble.connect(element)
                                print("Connected")
                                self.device=element
                                self.bleConnectionStatus="Connected"
                                self.updateStatus()
                                worker=Worker(self.isConnectedBLE)
                                worker.signals.finished.connect(self.finish)
                                print("Starting hb")
                                self.threadpool.start(worker)
                                break

                            else:
                                raise Exception("No UART service")
                        except:
                            self.showError("No UART service")
                        
                        

                        

    


    """
    Connect logic
    It needs threads since we
    """
    def scanPort(self):

        # scanning label
        #self.scanLbl.setText("Scanning...")
        #self.scanButton.setEnabled(False)
        print("Scanning...")
        
        self.ongoing="Scanning"
        self.updateStatus()
        
        self.scanLbl.setVisible(True)
        self.movie.start()
        self.bleConnectionStatus="Scanning"
        self.updateStatus()

        self.scanHandle()
        

    def scan(self):
        
        ble = BLERadio()
        print("scanning")
        found = set()
        scan_responses = set()

        self.comlist=[]

        # By providing Advertisement as well we include everything, not just specific advertisements.
        for advertisement in ble.start_scan(ProvideServicesAdvertisement,Advertisement,timeout=10):
            addr = advertisement.address
            if advertisement.scan_response and addr not in scan_responses:
                scan_responses.add(addr)
            elif not advertisement.scan_response and addr not in found:
                found.add(addr)
            else:
                continue
            print(addr, advertisement)
            
            #print(advertisement.)
            self.comlist.append(advertisement)

            print("\t" + repr(advertisement))
            print()
            

        print("scan done")
        


        connected = []
        self.dropdown.clear()
        for element in self.comlist:
            if element.complete_name==None:

                if element.address not in connected:
                    connected.append(element.address)
                    element.address.__str__()
                    #we need to remove out : Address(string=" and ")
                    self.dropdown.addItem(element.address.__str__()[16:-2])
            else:
                if element.complete_name not in connected:    
                    connected.append(element.complete_name)
                    self.dropdown.addItem(element.complete_name)


    def scanHandle(self):
        worker=Worker(self.scan)
        worker.signals.finished.connect(self.scanDone)
        self.threadpool.start(worker)
    

    def scanDone(self):
        
        self.movie.stop()
        self.scanLbl.hide()
        if(self.dropdown.maxCount()):
            self.connectButton.setEnabled(True)
        self.bleConnectionStatus="Disconnected"
        self.updateStatus()
        print("Scan complete")

    def finish(self):
        print("Exited thread")


class scanThread(QThread,):
    def __init__(self):
        super().__init__()
        self.setupUI()
