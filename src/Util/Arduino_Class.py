#Super of Arduino Class

# Standard Libaries
import logging
import random
import string
import serial

# Project Specific Modules
#from src.Util.UART_Serial_class import UART_Serial
#from src.Util.File_Class import File

from Util.Serial_Communicator_Class import Serial_Communicator

log = logging.getLogger('open_controller_log.log')

class Arduino:

    #Constructor with passed port name
    def __init__(self, passed_port_name):
        self.serial_port_name = passed_port_name #taking in pass port name
        self.socket_port = random.randint(50000, 60000) #making random int for socket port connection
        self.ser = Serial_Communicator(passed_port_name, str(self.socket_port)) #starting uart class

    #Send Data Over Serial Port
    def Send_Serial(self, msg):
        log.info('Sending {} through arduino serial'.format(msg))
        self.ser.Send(msg)

    #Read Serial Response
    def Read_Serial(self):
        msg = self.ser.Read()
        log.info('Read {} from arduino serial'.format(msg))
        return msg

    def __del__(self):
        self.ser.__del__()
