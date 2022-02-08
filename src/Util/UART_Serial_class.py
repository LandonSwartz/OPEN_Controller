#Class wrapper for UART Serial Communication

'''
TODO:
- Need to check sending
- logging
- etc
'''

import serial
import codecs

class UART_Serial(object):
    """For communicating through TX/RX pins"""

    'Constructor'
    def __init__(self):
        self.ser = serial.Serial() #May try to set here everything
        #self.ser.Open_Port(portname)
        print('UART_Serial Created')

    'Opens Serial Port with passed port name'
    def Open_Port(self, portname):
        try:
            self.ser = serial.Serial(portname)
            self.ser.baudrate = 115200  # grbl baudrate
        except serial.SerialException:
            print("Serial port failed to open")
            return 0; #for failure to open port

    'Reads Data from Serial Port when called'
    def Read_Data(self):
        #data = self.ser.read(40)  # read ten bytes from port
        data = self.ser.readline() # reading to EOL char
        data_nor = codecs.decode(data)
        #data_string = str(data, 'UTF-8')
        print("Read: '{}' from serial port {}".format(data_nor, self.Get_Port_Name())) # may not need this
        return data_nor

    'Write passed data to serial port when called'
    def Write_Data(self, data):
        data_encode = data.encode('utf-8')
        print('sent: {}'.format(data_encode))
        self.ser.write(data_encode)

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
        self.Close_Port()
        print('Port closed')