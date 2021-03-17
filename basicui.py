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
        MainWindow.resize(1004, 594)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAutoFillBackground(False)
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
        self.scanLbl = QtWidgets.QLabel(self.ConnectTab)
        self.scanLbl.setGeometry(QtCore.QRect(380, 170, 111, 17))
        self.scanLbl.setObjectName("scanLbl")
        self.tabWidget.addTab(self.ConnectTab, "")
        self.PrimingTab = QtWidgets.QWidget()
        self.PrimingTab.setObjectName("PrimingTab")
        self.startPrimeBtn = QtWidgets.QPushButton(self.PrimingTab)
        self.startPrimeBtn.setGeometry(QtCore.QRect(220, 30, 161, 51))
        self.startPrimeBtn.setObjectName("startPrimeBtn")
        self.rotateBtn = QtWidgets.QPushButton(self.PrimingTab)
        self.rotateBtn.setGeometry(QtCore.QRect(220, 100, 161, 51))
        self.rotateBtn.setObjectName("rotateBtn")
        self.countTxt = QtWidgets.QLabel(self.PrimingTab)
        self.countTxt.setGeometry(QtCore.QRect(310, 330, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.countTxt.setFont(font)
        self.countTxt.setObjectName("countTxt")
        self.lblcnt = QtWidgets.QLabel(self.PrimingTab)
        self.lblcnt.setGeometry(QtCore.QRect(184, 330, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lblcnt.setFont(font)
        self.lblcnt.setObjectName("lblcnt")
        self.finishPrimeBtn = QtWidgets.QPushButton(self.PrimingTab)
        self.finishPrimeBtn.setGeometry(QtCore.QRect(100, 410, 121, 51))
        self.finishPrimeBtn.setObjectName("finishPrimeBtn")
        self.fixedPrimeBtn = QtWidgets.QPushButton(self.PrimingTab)
        self.fixedPrimeBtn.setGeometry(QtCore.QRect(220, 240, 161, 51))
        self.fixedPrimeBtn.setObjectName("fixedPrimeBtn")
        self.toggleClutchBtn = QtWidgets.QPushButton(self.PrimingTab)
        self.toggleClutchBtn.setGeometry(QtCore.QRect(220, 170, 161, 51))
        self.toggleClutchBtn.setObjectName("toggleClutchBtn")
        self.resetBtn = QtWidgets.QPushButton(self.PrimingTab)
        self.resetBtn.setGeometry(QtCore.QRect(360, 410, 121, 51))
        self.resetBtn.setObjectName("resetBtn")
        self.primingBar = QtWidgets.QProgressBar(self.PrimingTab)
        self.primingBar.setGeometry(QtCore.QRect(390, 240, 131, 51))
        self.primingBar.setProperty("value", 24)
        self.primingBar.setObjectName("primingBar")
        self.tabWidget.addTab(self.PrimingTab, "")
        self.RecurringTab = QtWidgets.QWidget()
        self.RecurringTab.setObjectName("RecurringTab")
        self.label_2 = QtWidgets.QLabel(self.RecurringTab)
        self.label_2.setGeometry(QtCore.QRect(50, 270, 58, 18))
        self.label_2.setObjectName("label_2")
        self.outTxt = QtWidgets.QPlainTextEdit(self.RecurringTab)
        self.outTxt.setGeometry(QtCore.QRect(50, 310, 401, 191))
        self.outTxt.setObjectName("outTxt")
        self.startDoseBtn = QtWidgets.QPushButton(self.RecurringTab)
        self.startDoseBtn.setGeometry(QtCore.QRect(190, 210, 88, 34))
        self.startDoseBtn.setObjectName("startDoseBtn")
        self.doseTxt = QtWidgets.QTextEdit(self.RecurringTab)
        self.doseTxt.setGeometry(QtCore.QRect(340, 40, 104, 81))
        self.doseTxt.setObjectName("doseTxt")
        self.doseLbl = QtWidgets.QLabel(self.RecurringTab)
        self.doseLbl.setGeometry(QtCore.QRect(460, 50, 67, 17))
        self.doseLbl.setObjectName("doseLbl")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.RecurringTab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 40, 160, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.basalBtn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.basalBtn.setCheckable(True)
        self.basalBtn.setChecked(False)
        self.basalBtn.setObjectName("basalBtn")
        self.verticalLayout.addWidget(self.basalBtn)
        self.bolusBtn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.bolusBtn.setObjectName("bolusBtn")
        self.verticalLayout.addWidget(self.bolusBtn)
        self.deliveryAmtLbl = QtWidgets.QLabel(self.RecurringTab)
        self.deliveryAmtLbl.setGeometry(QtCore.QRect(360, 46, 131, 51))
        self.deliveryAmtLbl.setWordWrap(True)
        self.deliveryAmtLbl.setObjectName("deliveryAmtLbl")
        self.pulseDelayTxt = QtWidgets.QTextEdit(self.RecurringTab)
        self.pulseDelayTxt.setGeometry(QtCore.QRect(220, 110, 131, 70))
        self.pulseDelayTxt.setObjectName("pulseDelayTxt")
        self.deliveryAmtTxt = QtWidgets.QTextEdit(self.RecurringTab)
        self.deliveryAmtTxt.setGeometry(QtCore.QRect(360, 110, 121, 70))
        self.deliveryAmtTxt.setObjectName("deliveryAmtTxt")
        self.pulseDelayLbl = QtWidgets.QLabel(self.RecurringTab)
        self.pulseDelayLbl.setGeometry(QtCore.QRect(220, 40, 131, 61))
        self.pulseDelayLbl.setTextFormat(QtCore.Qt.AutoText)
        self.pulseDelayLbl.setScaledContents(False)
        self.pulseDelayLbl.setWordWrap(True)
        self.pulseDelayLbl.setObjectName("pulseDelayLbl")
        self.tabWidget.addTab(self.RecurringTab, "")
        self.CommandsTab = QtWidgets.QWidget()
        self.CommandsTab.setObjectName("CommandsTab")
        self.cmdTxt = QtWidgets.QTextEdit(self.CommandsTab)
        self.cmdTxt.setGeometry(QtCore.QRect(43, 140, 271, 31))
        self.cmdTxt.setObjectName("cmdTxt")
        self.cmdOutTxt = QtWidgets.QPlainTextEdit(self.CommandsTab)
        self.cmdOutTxt.setGeometry(QtCore.QRect(40, 230, 281, 191))
        self.cmdOutTxt.setObjectName("cmdOutTxt")
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
        self.BolusTestingTab = QtWidgets.QWidget()
        self.BolusTestingTab.setObjectName("BolusTestingTab")
        self.startBolusBtn = QtWidgets.QPushButton(self.BolusTestingTab)
        self.startBolusBtn.setGeometry(QtCore.QRect(40, 160, 131, 121))
        self.startBolusBtn.setObjectName("startBolusBtn")
        self.stopBolusBtn = QtWidgets.QPushButton(self.BolusTestingTab)
        self.stopBolusBtn.setGeometry(QtCore.QRect(330, 160, 131, 121))
        self.stopBolusBtn.setObjectName("stopBolusBtn")
        self.pulseDelayTxt_1 = QtWidgets.QTextEdit(self.BolusTestingTab)
        self.pulseDelayTxt_1.setGeometry(QtCore.QRect(40, 390, 131, 70))
        self.pulseDelayTxt_1.setObjectName("pulseDelayTxt_1")
        self.deliveryAmtTxt_1 = QtWidgets.QTextEdit(self.BolusTestingTab)
        self.deliveryAmtTxt_1.setGeometry(QtCore.QRect(340, 390, 121, 70))
        self.deliveryAmtTxt_1.setObjectName("deliveryAmtTxt_1")
        self.label_4 = QtWidgets.QLabel(self.BolusTestingTab)
        self.label_4.setGeometry(QtCore.QRect(40, 316, 131, 61))
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setScaledContents(False)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_8 = QtWidgets.QLabel(self.BolusTestingTab)
        self.label_8.setGeometry(QtCore.QRect(340, 326, 131, 51))
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.tabWidget.addTab(self.BolusTestingTab, "")
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(610, 30, 67, 17))
        self.statusLabel.setObjectName("statusLabel")
        self.statusTxt = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.statusTxt.setGeometry(QtCore.QRect(620, 60, 241, 251))
        self.statusTxt.setStyleSheet("background-color: rgb(239, 239, 239);")
        self.statusTxt.setReadOnly(True)
        self.statusTxt.setObjectName("statusTxt")
        self.stopAllBtn = QtWidgets.QPushButton(self.centralwidget)
        self.stopAllBtn.setGeometry(QtCore.QRect(618, 444, 371, 41))
        self.stopAllBtn.setObjectName("stopAllBtn")
        self.DisconnectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.DisconnectBtn.setGeometry(QtCore.QRect(620, 500, 371, 41))
        self.DisconnectBtn.setObjectName("DisconnectBtn")
        self.doseStatusTxt = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.doseStatusTxt.setGeometry(QtCore.QRect(620, 350, 371, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.doseStatusTxt.setFont(font)
        self.doseStatusTxt.setReadOnly(True)
        self.doseStatusTxt.setPlainText("")
        self.doseStatusTxt.setObjectName("doseStatusTxt")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(620, 320, 201, 17))
        self.label_6.setObjectName("label_6")
        self.connectionStatusLbl = QtWidgets.QLabel(self.centralwidget)
        self.connectionStatusLbl.setGeometry(QtCore.QRect(870, 60, 21, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(239, 41, 41))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 41, 41))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 41, 41))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 41, 41))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 41, 41))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 41, 41))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 41, 41))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 41, 41))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 41, 41))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.connectionStatusLbl.setPalette(palette)
        self.connectionStatusLbl.setAutoFillBackground(False)
        self.connectionStatusLbl.setStyleSheet("background-color: rgb(239, 41, 41)")
        self.connectionStatusLbl.setText("")
        self.connectionStatusLbl.setObjectName("connectionStatusLbl")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1004, 22))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Insulin Delivery"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.scanButton.setText(_translate("MainWindow", "Scan"))
        self.scanLbl.setText(_translate("MainWindow", "Scanning..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ConnectTab), _translate("MainWindow", "Connect"))
        self.startPrimeBtn.setText(_translate("MainWindow", "Start priming"))
        self.rotateBtn.setText(_translate("MainWindow", "Rotate"))
        self.countTxt.setText(_translate("MainWindow", "0"))
        self.lblcnt.setText(_translate("MainWindow", "Count:"))
        self.finishPrimeBtn.setText(_translate("MainWindow", "Finish priming"))
        self.fixedPrimeBtn.setText(_translate("MainWindow", "Fixed Prime"))
        self.toggleClutchBtn.setText(_translate("MainWindow", "Toggle Clutch"))
        self.resetBtn.setText(_translate("MainWindow", "Reset"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PrimingTab), _translate("MainWindow", "Priming"))
        self.label_2.setText(_translate("MainWindow", "Output"))
        self.startDoseBtn.setText(_translate("MainWindow", "Start"))
        self.doseLbl.setText(_translate("MainWindow", "IU/hr"))
        self.basalBtn.setText(_translate("MainWindow", "Basal"))
        self.bolusBtn.setText(_translate("MainWindow", "Bolus"))
        self.deliveryAmtLbl.setText(_translate("MainWindow", "Delivery amount in IU"))
        self.pulseDelayLbl.setText(_translate("MainWindow", "Duration Between Pulses(in milliseconds)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RecurringTab), _translate("MainWindow", "Recurring commands"))
        self.label.setText(_translate("MainWindow", "Output"))
        self.label_5.setText(_translate("MainWindow", "Command"))
        self.SendButton.setText(_translate("MainWindow", "Send"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CommandsTab), _translate("MainWindow", "Command"))
        self.startBolusBtn.setText(_translate("MainWindow", "Start"))
        self.stopBolusBtn.setText(_translate("MainWindow", "Stop"))
        self.label_4.setText(_translate("MainWindow", "Duration Between Pulses(in milliseconds)"))
        self.label_8.setText(_translate("MainWindow", "Delivery amount in IU"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.BolusTestingTab), _translate("MainWindow", "Bolus Testing"))
        self.statusLabel.setText(_translate("MainWindow", "Status"))
        self.stopAllBtn.setText(_translate("MainWindow", "Stop"))
        self.DisconnectBtn.setText(_translate("MainWindow", "Disconnect"))
        self.label_6.setText(_translate("MainWindow", "Current Ongoing Delivery:"))
