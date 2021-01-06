import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer,QThreadPool,QThread
import serial
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

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

        #status area
        self.statusTxt=self.ui.statusTxt
        
        self.stopAllBtn=self.ui.stopAllBtn
        self.stopAllBtn.clicked.connect(self.stop)
        
        self.disconnectBtn =self.ui.DisconnectBtn

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
    
    def showDialog(self,cmd):
    	msgBox = QMessageBox()
    	msgBox.setIcon(QMessageBox.Information)
    	msgBox.setText("Send command "+cmd+" ?")
    	msgBox.setWindowTitle("Message")
    	msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    	#msgBox.buttonClicked.connect(msgButtonClick) 
    	returnValue = msgBox.exec()
    	if returnValue == QMessageBox.Ok:
    		print('OK clicked')
    
    def stop(self):
        #do one rotation
        self.showDialog("Stop")
        pass

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec())

