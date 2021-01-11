import os
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout, QProgressBar, QVBoxLayout,QLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QMovie

from multithread import Worker,WorkerSignals

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


        

        self.scanLbl=self.ui.scanLbl
        
        self.scanLbl.setText("")

        self.movie = QMovie("loader.gif")
        self.scanLbl.setMovie(self.movie)        

    def isConnectedBLE(self):
        #check for heartbeat here
        pass

        return 0

    def isConnectedReciever(self):
        #checks if bluetooth reciever is connected
        #if(os.system("timeout -s INT 1s hcitool lescan")== 256):
        
        return 0
        return 1


    def chk(self):
        #enable tabs
        #se lf.ui.tabWidget.setTabEnabled(1,self.isConnectedBLE())
        #self.ui.tabWidget.setTabEnabled(2,self.isConnectedBLE())
        pass


    def connectPort(self):
        if(self.dropdown.currentText()):
            self.port=self.dropdown.currentText()
            
            """
            #add logic to pair with BLE
            """

            print("Connected to:"+self.dropdown.currentText())
    
    def scanPort(self):

        #scanning label
        #self.scanLbl.setText("Scanning...")
        #self.scanButton.setEnabled(False)
        print("Scanning...")
        
        self.ongoing="Scanning"
        self.updateStatus()
        
        if(self.isConnectedReciever()):
            self.updateStatus()
            return 0
        self.movie.start()

        self.scanHandle()
        

    def scan(self):
        cmd=os.popen("timeout -s INT 10s hcitool lescan")

        comlist = cmd.read()
        
        comlist = comlist.split('\n')
        print(comlist)
        
        #the fist and last element is empty 
        comlist.pop(0)
        comlist.pop()

        connected = []
        self.dropdown.clear()
        for element in comlist:
            if element not in connected:
                connected.append(element)
                self.dropdown.addItem(element)


    def scanHandle(self):
        worker=Worker(self.scan)
        worker.signals.finished.connect(self.scanDone)
        self.threadpool.start(worker)
    

    def scanDone(self):
        self.movie.stop()
        self.scanLbl.hide()
        self.connectButton.setEnabled(True)
        print("Scan complete")
