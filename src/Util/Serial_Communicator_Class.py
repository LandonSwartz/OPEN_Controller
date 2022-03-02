#Combines serial class and serial listener process to create serial event loop

import subprocess
import socket
from time import sleep
#from signal import SIGINT
from signal import CTRL_C_EVENT

#TODO change CTRL_C_EVENT to SIGINT in UNIX

class Serial_Communicator:

    'Constructor'
    def __init__(self, portname, socket_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.args = ['python', 'Util/Serial_Listener.py']

        # passing args to process
        self.args.append(portname)
        self.args.append(socket_port)
        print(self.args)

        # start serial process
        self.p = subprocess.Popen(self.args, shell=True) #may add the shell part
        print('pid for serial communicator process', self.p.pid)
        sleep(0.1)

        #starting socket
        self.s.bind(('127.0.0.1', int(socket_port))) #setting server socket with passing
        try:
            self.s.listen()
            self.conn, self.addr = self.s.accept()
        except socket.timeout:
            print('Timed out for client socket connection')
        self.s.settimeout(0.1) #timeout set to 0.1 millisecond after connecting

    #sends to serial
    def Send(self, msg):
        msg_byte = self.ConvertToBytes(msg)
        self.conn.send(msg_byte)

    #recieve from serial
    def Read(self):
        try:
            bytes_rec = self.conn.recv(1024)
            if bytes_rec:
                string = self.ConvertToString(bytes_rec)
                return string
            else:
                return None
        except TimeoutError:
            print('timeout from reading to serial in serial communicator')


    # Converting string to bytes to send over socket
    def ConvertToBytes(self, string):
        return bytes(string, 'UTF-8') #converting to bytes

    # Convert bytes receieved to string
    def ConvertToString(self, bytes):
        return str(bytes, 'UTF-8')

    def __del__(self):
        try:
            self.p.send_signal(CTRL_C_EVENT) #sending interupt signals to python script to close serial, change to UNIX SIGINT in future
            self.p.terminate() #may need to do p.kill()
            self.conn.close() #close socket
        except:
            print('failure to delete class properly')