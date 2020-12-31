import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer,QThreadPool,QThread
import serial
from basicui import Ui_MainWindow
import serial.tools.list_ports
from datetime import datetime as dt
from _connectTab import connectTab
from _primingTab import primingTab
from _commandTab import commandTab
from _recurringTab import recurringTab

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow,connectTab,primingTab,commandTab,recurringTab):
    def __init__(self, *args, obj=None, **kwargs):
        
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.statusTxt=self.ui.statusTxt
        
        #initialize threading
        self.threadpool=QThreadPool


        self.port=""
        

        self.init_connectTab()

        
        self.init_primingTab()
        
        self.init_commandTab()

        self.init_recurringTab()

        self.rotations=0
        self.ongoing= self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        
        self.updateStatus()

    def updateStatus(self):
        self.statusTxt.clear()
        self.statusTxt.appendPlainText("Reciever Status:" +  ("Connected" if self.isConnectedReciever() else "Disconnected" ))
        self.statusTxt.appendPlainText("BLE Status:" + ("Connected" if self.isConnectedBLE() else "Disconnected") )
        self.statusTxt.appendPlainText("Rotations: " + str(self.rotations))
        self.statusTxt.appendPlainText("Ongoing:"+ self.ongoing)
        

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()