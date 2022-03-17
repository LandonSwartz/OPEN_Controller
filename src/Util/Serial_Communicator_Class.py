#Combines serial class and serial listener process to create serial event loop
import logging
import subprocess
import socket
import sys
from time import sleep
#from signal import SIGINT
from signal import CTRL_C_EVENT

#TODO change CTRL_C_EVENT to SIGINT in UNIX

log = logging.getLogger('open_controller_log.log')

class Serial_Communicator:

    'Constructor'
    def __init__(self, portname, socket_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sys.platform is 'Linux':
            self.args = ['python3', 'Util/Serial_Listener.py']  # python3 for unix
        elif sys.platform is 'Win32':   # double check in future that this works
            self.args = ['python', 'Util/Serial_Listener.py']    # python for windows

        # passing args to process
        self.args.append(portname)
        self.args.append(socket_port)

        # start serial process
        self.p = subprocess.Popen(self.args) #may add the shell part
        log.info('Serial communicator subprocess pid is {}'.format(self.p.pid))
        sleep(0.1)

        #starting socket
        self.s.bind(('localhost', int(socket_port))) #setting server socket with passing
        try:
            self.s.listen()
            self.conn, self.addr = self.s.accept()
            log.debug('Socket connected to port {} on localhost'.format(socket_port))
        except socket.timeout:
            log.error('Timed out for client socket connection at port {}'.format(socket_port))
        self.s.settimeout(1) #timeout set to 1 millisecond after connecting

    # sends to serial
    def Send(self, msg):
        log.info('Sending {} from to serial socket'.format(msg))
        msg_byte = self.ConvertToBytes(msg)
        self.conn.send(msg_byte)

    # receive from serial
    def Read(self):
        try:
            bytes_rec = self.conn.recv(1024)    # receive bytes
            if bytes_rec:
                string = self.ConvertToString(bytes_rec)
                #print("read from serial communicator: " + string)
                log.info("Read: {}, from serial port in serial communciator",format(string))
                return string
            else:
                log.debug('Nothing was read from the serial port')
                return None
        except TimeoutError as e:
            log.error('{} trying to read from socket in serial communicator'.format(e))

    # Converting string to bytes to send over socket
    def ConvertToBytes(self, string):
        return bytes(string, 'UTF-8') #converting to bytes

    # Convert bytes receieved to string
    def ConvertToString(self, inc_bytes):
        return str(inc_bytes, 'UTF-8')

    def __del__(self):
        try:
            #self.p.send_signal(SIGINT) #sending interupt signals to python script to close serial
            self.p.send_signal(CTRL_C_EVENT) #sending interupt signals to python script to close serial, change to UNIX SIGINT in future
            self.p.terminate() #may need to do p.kill()
            self.conn.close() #close socket
            log.debug('Deleting Serial Communciator Class')
        except:
            log.error('Failure to close Serial Communicator Class properly')
