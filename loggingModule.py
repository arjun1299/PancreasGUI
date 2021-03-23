import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from queue import Queue


import time
import datetime
import sys
import logging
import os


class Logger(QThread):
    """
    Logging module which runs on a thread and keeps checking the queue for checking processes and adding it into the queue
    """
    q=Queue()
    loggerError=pyqtSignal()

    def __init__(self):
        
        super().__init__()

        name=datetime.datetime.now()
        name = name.strftime("%d-%m-%Y, %H:%M")
        logging.basicConfig(filename=name,format='%(levelname)s %(asctime)s.%(msecs)03d - %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)
        os.chmod(name, 0o777)
        if not logging.getLogger().hasHandlers():
            self.loggerError.emit()
            print("Logger Error!")
            time.sleep(10)
            exit()



        logging.warning("Started")

    def run(self):
        Logger.q.put(("INFO","Starting logger"))
        print("Starting logger")
        
        while 1:
            while self.q.empty()==False :
                temp1=current_milli_time()
                (level,message)= Logger.q.get()
                if message=="Stop":
                    break
                print("Logged!"+ level + message )

                """
                
                Split into differenent logging levels
                """

                if(level=="WARNING"):
                    logging.warning(message)
                elif(level=="ERROR"):
                    logging.error(message)
                elif(level=="INFO"):
                    logging.info(message)
                temp2=current_milli_time()
                print("LOGGER TIME: ",temp2-temp1)
            
            time.sleep(0.0005)

def current_milli_time():
    return round(time.time() * 1000)
