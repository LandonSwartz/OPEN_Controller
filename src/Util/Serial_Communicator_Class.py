#Combines serial class and serial listener process to create serial event loop
import logging
import subprocess
import socket
from time import sleep
from signal import SIGINT
#from signal import CTRL_C_EVENT

#TODO change CTRL_C_EVENT to SIGINT in UNIX

log = logging.getLogger('open_controller_log.log')

class Serial_Communicator:

    'Constructor'
    def __init__(self, portname, socket_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.args = ['python3', 'Util/Serial_Listener.py']

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
        self.s.settimeout(0.1) #timeout set to 0.1 millisecond after connecting

    #sends to serial
    def Send(self, msg):
        log.info('Sending {} from to serial socket'.format(msg))
        msg_byte = self.ConvertToBytes(msg)
        self.conn.send(msg_byte)

    #recieve from serial
    def Read(self):
        try:
            bytes_rec = self.conn.recv(1024)
            if bytes_rec:
                string = self.ConvertToString(bytes_rec)
                print("read from serial communicator: " + string)
                return string
            else:
                return None
        except TimeoutError as e:
            log.error('{} trying to read from socket in serial communicator'.format(e))
            print('timeout from reading to serial in serial communicator')


    # Converting string to bytes to send over socket
    def ConvertToBytes(self, string):
        return bytes(string, 'UTF-8') #converting to bytes

    # Convert bytes receieved to string
    def ConvertToString(self, bytes):
        return str(bytes, 'UTF-8')

    def __del__(self):
        try:
            self.p.send_signal(SIGINT) #sending interupt signals to python script to close serial, change to UNIX SIGINT in future
            self.p.terminate() #may need to do p.kill()
            self.conn.close() #close socket
            log.debug('Deleting Serial Communciator Class')
        except:
            print('failure to delete class properly')