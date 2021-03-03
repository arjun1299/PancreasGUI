import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from queue import Queue


import time
import sys
import logging


class Logger(QThread):
    """
    Logging module which runs on a thread and keeps checking the queue for checking processes and adding it into the queue
    """
    q=Queue()

    def __init__(self):
        super().__init__()
        logging.basicConfig(filename="log.txt",format='%(levelname)s %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)
        logging.warning("Started")

    def run(self):
        Logger.q.put(("INFO","Starting logger"))
        print("Starting logger")
        
        while 1:
            if self.q.empty()==False :
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

            time.sleep(0.005)

def current_milli_time():
    return round(time.time() * 1000)
