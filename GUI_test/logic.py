from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from untitled import Ui_MainWindow

import time
import traceback, sys
import os


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        
        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done



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

    def scan(self):
        cmd=os.popen("timeout -s INT 10s hcitool lescan")
        print(cmd.read())


    def scanHandle(self):
        worker=Worker(self.scan)
        self.threadpool.start(worker)

    def threadHandle(self,fun):
        worker=Worker(fun)
        self.threadpool.start(worker)
        worker.signals.finished.connect(self.finished)
    

    def loopHandle(self):
        worker=Worker(self.looper)
        worker.signals.finished.connect(self.finished)

        self.threadpool.start(worker)
        
    def finished(self):
        print("Done!!!!!!!!!!!!!")

    def looper(self):
        count=0
        while count!=100:
            print("Hello" + str(self.threadpool.activeThreadCount()))
            count+=1
            time.sleep(0.1)




app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
