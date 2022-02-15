#Class wrapper for UART Serial Communication

'''
TODO:
- Need to check sending
- logging
- etc
'''

'''To try next: interprocess communication with spinning off serial listener into new process with fork(), execfile()
or subprocess. Communicate between the processes with named pipe (os.mkfifo) or multi-threading communicator'''

import serial
import threading
from queue import Queue

# may do events for when recieving data causing data to be sent
import codecs

class UART_Serial(object):
    """For communicating through TX/RX pins"""
    to_send_queue = Queue(maxsize=0) #sending queue
    to_read_queue = Queue(maxsize=0) #reading queue

    'Constructor'
    def __init__(self):
        self.ser = serial.Serial() #May try to set here everything
        #self.ser.Open_Port(portname)
        print('UART_Serial Created')
        #listening thread
        self.listening_thread = threading.Thread(self.Listening_To_Serial(), daemon=True)
        self.sending_thread = threading.Thread(self.Sending_Serial(), daemon=True)
        self._lock = threading.Lock() #lock for thread


    'Opens Serial Port with passed port name'
    def Open_Port(self, portname):
        try:
            self.ser = serial.Serial(portname)
            self.ser.baudrate = 115200  # grbl baudrate
        except serial.SerialException:
            print("Serial port failed to open")
            return 0  # for failure to open port

    #May not need
    # Get all contents of to read queue
    def To_Read_Data(self):
        return self.to_read_queue #send to read queue to requested

    #Add To Send Data
    def To_Send_Data(self, msg):
        self.to_send_queue.put(msg)

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

    'Threading Functions for listening and sending'
    # useful link: https://realpython.com/intro-to-python-threading/
    # function that will be passed to thread in inition for
    def Listening_To_Serial(self):
        to_read_local = self.to_read_queue
        while(True):
            #passing local copies
            #ser_local = self.ser #don't know if needed because not changing data
            if(self.ser.in_waiting > 0):  # if something in serial port, read it
                with self._lock: # acquiring lock
                    to_read_local.put(self.Read_Data())
                    #self.to_read_queue.put(self.Read_Data())  # putting into queue
                    self.to_read_queue = to_read_local

    # thread function for sending serial data
    #TODO check this thread for working with local copy of to send queue
    def Sending_Serial(self):
        #to_send_local = self.to_send_queue
        while(True):
            if(self.to_send_queue.empty() == False):
                with self._lock:  # acquiring and releasing lock
                    self.Write_Data(self.to_send_queue.get()) # send data from queue

    'Deconstructor, closes port on exit'
    def __del__(self):
        # joining daemon threads
        self.listening_thread.join()
        self.sending_thread.join()
        # closing port
        self.Close_Port()
        print('Port closed')