import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from queue import Queue


import time
import sys
import logging


global LOG
LOG=False


class Parser(QThread):
    """
    Logging module which runs on a thread and keeps checking the queue for checking processes and adding it into the queue
    """
    q=Queue()

    def run(self):
        
        while 1:
            if self.q.empty()==False :
                s= Parser.q.get()
                if s=="Stop":
                    break
                print("Parsed!"+ s )
                
            time.sleep(0.1)