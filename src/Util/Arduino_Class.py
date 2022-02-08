#Super of Arduino Class

import string

import serial

from src.Util.UART_Serial_class import UART_Serial
from src.Util.File_Class import File

class Arduino(object):
    serial_port_name: string
    serial = UART_Serial()
    settings_file = File('src/GRBL_settings.txt')

    #Constructor
    def __init__(self):
        print('arduino initiated')
        self.Open_Serial()

    #Constructor with passed port name
    def __init__(self, passed_port_name):
        self.serial_port_name = passed_port_name
        self.Open_Serial(passed_port_name)

    #Open Serial Port with passed port_name
    def Open_Serial(self, port_name):
        try:
            self.serial.Open_Port(port_name)
        except serial.SerialException as e:
            print('Serial Port {} was not able to connect because {}'.format(port_name, e))

    #Open Serial Port with port name with set port name
    def Open_Serial(self):
        try:
            self.serial.Open_Port(self.serial_port_name)
        except serial.SerialException as e:
            print('Serial Port {} was not able to connect because {}'.format(self.serial_port_name, e))

    #Send Data Over Serial Port
    def Send_Serial(self, msg):
        self.serial.Write_Data(msg)

    #Read Serial Response
    def Read_Serial(self):
        msg = self.serial.Read_Data()
        return msg

    def __del__(self):
        self.serial.__del__()
