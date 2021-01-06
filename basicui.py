# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basic.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(802, 591)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 601, 551))
        self.tabWidget.setObjectName("tabWidget")
        self.ConnectTab = QtWidgets.QWidget()
        self.ConnectTab.setObjectName("ConnectTab")
        self.connectButton = QtWidgets.QPushButton(self.ConnectTab)
        self.connectButton.setGeometry(QtCore.QRect(190, 240, 88, 34))
        self.connectButton.setObjectName("connectButton")
        self.comboBox = QtWidgets.QComboBox(self.ConnectTab)
        self.comboBox.setGeometry(QtCore.QRect(80, 160, 291, 32))
        self.comboBox.setObjectName("comboBox")
        self.scanButton = QtWidgets.QPushButton(self.ConnectTab)
        self.scanButton.setGeometry(QtCore.QRect(310, 240, 88, 34))
        self.scanButton.setObjectName("scanButton")
        self.tabWidget.addTab(self.ConnectTab, "")
        self.PrimingTab = QtWidgets.QWidget()
        self.PrimingTab.setObjectName("PrimingTab")
        self.startPrime = QtWidgets.QPushButton(self.PrimingTab)
        self.startPrime.setGeometry(QtCore.QRect(100, 160, 121, 51))
        self.startPrime.setObjectName("startPrime")
        self.rotateBtn = QtWidgets.QPushButton(self.PrimingTab)
        self.rotateBtn.setGeometry(QtCore.QRect(330, 120, 161, 51))
        self.rotateBtn.setObjectName("rotateBtn")
        self.countTxt = QtWidgets.QLabel(self.PrimingTab)
        self.countTxt.setGeometry(QtCore.QRect(270, 310, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.countTxt.setFont(font)
        self.countTxt.setObjectName("countTxt")
        self.lblcnt = QtWidgets.QLabel(self.PrimingTab)
        self.lblcnt.setGeometry(QtCore.QRect(144, 310, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lblcnt.setFont(font)
        self.lblcnt.setObjectName("lblcnt")
        self.finishPrimeBtn = QtWidgets.QPushButton(self.PrimingTab)
        self.finishPrimeBtn.setGeometry(QtCore.QRect(200, 420, 121, 51))
        self.finishPrimeBtn.setObjectName("finishPrimeBtn")
        self.clutchBtn = QtWidgets.QPushButton(self.PrimingTab)
        self.clutchBtn.setGeometry(QtCore.QRect(330, 200, 161, 51))
        self.clutchBtn.setObjectName("clutchBtn")
        self.tabWidget.addTab(self.PrimingTab, "")
        self.RecurringTab = QtWidgets.QWidget()
        self.RecurringTab.setObjectName("RecurringTab")
        self.label_2 = QtWidgets.QLabel(self.RecurringTab)
        self.label_2.setGeometry(QtCore.QRect(50, 270, 58, 18))
        self.label_2.setObjectName("label_2")
        self.reOut = QtWidgets.QPlainTextEdit(self.RecurringTab)
        self.reOut.setGeometry(QtCore.QRect(50, 310, 401, 191))
        self.reOut.setObjectName("reOut")
        self.SetButton = QtWidgets.QPushButton(self.RecurringTab)
        self.SetButton.setGeometry(QtCore.QRect(350, 210, 88, 34))
        self.SetButton.setObjectName("SetButton")
        self.basalBtn = QtWidgets.QPushButton(self.RecurringTab)
        self.basalBtn.setGeometry(QtCore.QRect(60, 60, 261, 41))
        self.basalBtn.setObjectName("basalBtn")
        self.pushButton_2 = QtWidgets.QPushButton(self.RecurringTab)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 140, 261, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.basalTxt = QtWidgets.QTextEdit(self.RecurringTab)
        self.basalTxt.setGeometry(QtCore.QRect(350, 60, 104, 41))
        self.basalTxt.setObjectName("basalTxt")
        self.bolusTxt = QtWidgets.QTextEdit(self.RecurringTab)
        self.bolusTxt.setGeometry(QtCore.QRect(350, 140, 104, 41))
        self.bolusTxt.setObjectName("bolusTxt")
        self.label_3 = QtWidgets.QLabel(self.RecurringTab)
        self.label_3.setGeometry(QtCore.QRect(470, 80, 67, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.RecurringTab)
        self.label_4.setGeometry(QtCore.QRect(470, 160, 67, 17))
        self.label_4.setObjectName("label_4")
        self.cmdTxt_2 = QtWidgets.QTextEdit(self.RecurringTab)
        self.cmdTxt_2.setGeometry(QtCore.QRect(60, 210, 261, 31))
        self.cmdTxt_2.setObjectName("cmdTxt_2")
        self.tabWidget.addTab(self.RecurringTab, "")
        self.CommandsTab = QtWidgets.QWidget()
        self.CommandsTab.setObjectName("CommandsTab")
        self.cmdTxt = QtWidgets.QTextEdit(self.CommandsTab)
        self.cmdTxt.setGeometry(QtCore.QRect(43, 140, 271, 31))
        self.cmdTxt.setObjectName("cmdTxt")
        self.outTxt = QtWidgets.QPlainTextEdit(self.CommandsTab)
        self.outTxt.setGeometry(QtCore.QRect(40, 230, 281, 191))
        self.outTxt.setObjectName("outTxt")
        self.label = QtWidgets.QLabel(self.CommandsTab)
        self.label.setGeometry(QtCore.QRect(50, 200, 58, 18))
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.CommandsTab)
        self.label_5.setGeometry(QtCore.QRect(40, 110, 111, 18))
        self.label_5.setObjectName("label_5")
        self.SendButton = QtWidgets.QPushButton(self.CommandsTab)
        self.SendButton.setGeometry(QtCore.QRect(340, 140, 88, 34))
        self.SendButton.setObjectName("SendButton")
        self.tabWidget.addTab(self.CommandsTab, "")
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(610, 30, 67, 17))
        self.statusLabel.setObjectName("statusLabel")
        self.statusTxt = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.statusTxt.setGeometry(QtCore.QRect(610, 60, 181, 371))
        self.statusTxt.setObjectName("statusTxt")
        self.stopAllBtn = QtWidgets.QPushButton(self.centralwidget)
        self.stopAllBtn.setGeometry(QtCore.QRect(618, 444, 171, 41))
        self.stopAllBtn.setObjectName("stopAllBtn")
        self.DisconnectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.DisconnectBtn.setGeometry(QtCore.QRect(620, 500, 171, 41))
        self.DisconnectBtn.setObjectName("DisconnectBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.scanButton.setText(_translate("MainWindow", "Scan"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ConnectTab), _translate("MainWindow", "Connect"))
        self.startPrime.setText(_translate("MainWindow", "Start priming"))
        self.rotateBtn.setText(_translate("MainWindow", "Rotate"))
        self.countTxt.setText(_translate("MainWindow", "0"))
        self.lblcnt.setText(_translate("MainWindow", "Count:"))
        self.finishPrimeBtn.setText(_translate("MainWindow", "Finish priming"))
        self.clutchBtn.setText(_translate("MainWindow", "Engage clutch"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PrimingTab), _translate("MainWindow", "Priming"))
        self.label_2.setText(_translate("MainWindow", "Output"))
        self.SetButton.setText(_translate("MainWindow", "Send"))
        self.basalBtn.setText(_translate("MainWindow", "Basal"))
        self.pushButton_2.setText(_translate("MainWindow", "Bolus"))
        self.label_3.setText(_translate("MainWindow", "Iu/hr"))
        self.label_4.setText(_translate("MainWindow", "Iu"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RecurringTab), _translate("MainWindow", "Recurring commands"))
        self.label.setText(_translate("MainWindow", "Output"))
        self.label_5.setText(_translate("MainWindow", "Command"))
        self.SendButton.setText(_translate("MainWindow", "Send"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CommandsTab), _translate("MainWindow", "Command"))
        self.statusLabel.setText(_translate("MainWindow", "Status"))
        self.stopAllBtn.setText(_translate("MainWindow", "Stop"))
        self.DisconnectBtn.setText(_translate("MainWindow", "Disconnect"))
