#Class wrapper for UART Serial Communication

'''
TODO:
- Need to check sending
- logging
- etc
'''

import serial
import threading
from queue import Queue
import subprocess
import socket

# may do events for when recieving data causing data to be sent
import codecs

class UART_Serial:

    'Constructor'
    def __init__(self):
        self.ser = serial.Serial() #May try to set here everything
        #self.ser.Open_Port(portname)
        print('UART_Serial Created')


    'Opens Serial Port with passed port name'
    def Open_Port(self, portname):
        try:
            print(portname)
            self.ser = serial.Serial(portname, timeout = 1, write_timeout = 0.1)
            self.ser.baudrate = 115200  # grbl baudrate
        except serial.SerialException:
            print("Serial port failed to open")
            return 0  # for failure to open port

    'Reads Data from Serial Port when called'
    def Read_Data(self):
        #data = []
        #if(self.ser.in_waiting > 0):
        line = self.ser.readline()
            #data.append(codecs.decode(line))
            #print(line)
        return bytes(line)

    'Write passed data to serial port when called'
    def Write_Data(self, data):
        #data_encode = data.encode('utf-8')
        #print('sent: {}'.format(data_encode))
        self.ser.write(data)
        
    def IsDataInSerial(self):
        #print(self.ser.in_waiting)
        return (self.ser.in_waiting > 0)

    """Get Baudrate of current open port"""
    def Get_Baudrate(self):
        return self.ser.baudrate

    """returns dictionary of current port settings"""
    """dict :return"""
    def Get_Settings(self):
        return self.ser.get_settings()

    """Set settings of serial port"""
    def Set_Settings(self, d):
        self.ser.apply_settings(d)

    """Flush of file like objects, wait until all data written"""
    def Flush_Port(self):
        self.ser.flush()

    'Closes Port when called'
    def Close_Port(self):
        print('Port {} is closed'.format(self.ser.name))
        self.ser.close()

    'Returns name of port when called'
    def Get_Port_Name(self):
        return self.ser.name

    'Deconstructor, closes port on exit'
    def __del__(self):
        # closing port
        self.Close_Port()
        print('Port closed')