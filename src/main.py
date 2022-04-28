#draft of OPEN Controller UI, actual design

import sys
#print(sys.path)

import tkinter as tk
from GUI.Main_Application import MainApplication
from Machine_Class import Machine

from time import sleep

#from Util.logger_setup import logger
import logging


def main():
    #maindow set up
    root = tk.Tk()
    root.title("OPEN Controller")
    #root.geometry('400x600') #set window size
    #root.resizable(False, False) #turning off resizing

    machine = Machine()

    app = MainApplication(root, machine)
    sleep(2)
    #run window
    app.mainloop()
    
    machine.__del__()

if __name__ == '__main__':
    logging.basicConfig(filename='open_controller_log.log',
                        level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    '''logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')'''
    logger = logging.getLogger('open_controller_log.log')
    logger.info('\n====== Application started and logging started ======')
    main()