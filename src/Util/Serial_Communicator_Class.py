#Combines serial class and serial listener process to create serial event loop
import logging
import subprocess
import socket
import sys
from time import sleep
#from signal import SIGINT
from signal import CTRL_C_EVENT
from threading import Thread

#TODO change CTRL_C_EVENT to SIGINT in UNIX

log = logging.getLogger('open_controller_log.log')

class Serial_Communicator:

    read_Queue = [] #reading qeueue
    send_Queue = [] #sending queue

    'Constructor'
    def __init__(self, portname, socket_port):

        #self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sys.platform == 'Linux':
            self.args = ['python3', 'Util/Serial_Listener.py']  # python3 for unix
        elif sys.platform == 'win32':   # double check in future that this works
            self.args = ['python', 'Util/Serial_Listener.py']    # python for windows

        # passing args to process
        self.args.append(portname)
        self.args.append(socket_port)

        # start serial process
        self.p = subprocess.Popen(self.args) #may add the shell part
        log.info('Serial communicator subprocess pid is {}'.format(self.p.pid))
        sleep(0.5)

        # starting socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('localhost', int(socket_port)))  # setting server socket with passing

        try:
            self.s.listen()
            self.conn, addr = self.s.accept()
            log.debug('Socket connected to port {} on localhost'.format(socket_port))
            # conn.send(b'$H\n')
        except socket.timeout:
            log.error('Timed out for client socket connection at port {}'.format(socket_port))
        self.s.settimeout(0.1)  # timeout set to 1 millisecond after connecting

        # starting daemon socket listener thread
        self.socket_listener = Thread(target=self.listener_thread, args=[socket_port, self.read_Queue, self.send_Queue])
        self.socket_listener.setDaemon(True)
        sleep(0.1)
        self.socket_listener.start()

    def listener_thread(self, socket_port, readq, writeq): #TODO check this functions ability to work
        logging.debug('Entered listener thread')
        running = True

        while running:
            try:
                data = self.conn.recv(1024)    # listening from socket
                if data: #if recieved something from socket
                    data_string = self.ConvertToString(data)
                    log.info("Read: {}, from serial port in serial communciator".format(data_string))
                    self.read_Queue.append(data_string)
            except socket.timeout: #instead of TimeoutError
                #log.debug('passing')
                pass
            except ConnectionResetError:
                running = False
            sleep(0.1)

            try:    # sending to socket (to send to serial)
                if len(self.send_Queue) > 0:
                    #log.debug('sending queue is {}'.format(self.send_Queue))
                    to_send = self.send_Queue.pop(0)
                    self.conn.send(to_send) #make sure this decreases size of qeueu
                    log.debug('socket just sent {} from send_queue'.format(to_send))
            except socket.timeout:
                pass
            #except ConnectionResetError:
                #running = False

            sleep(0.1)


    # sends to serial
    def Send(self, msg):
        msg_byte = self.ConvertToBytes(msg)
        self.send_Queue.append(msg_byte)
        log.debug(self.send_Queue)

    # receive from serial
    def Read(self):
        try:
            #log.debug(self.read_Queue)
            to_read = self.read_Queue.pop(0)
            #log.debug(self.read_Queue)
            #string = self.ConvertToString(to_read)
            return to_read
        except IndexError:
            #log.error('Read Queue in serial communicator is empty')
            return None

    # Converting string to bytes to send over socket
    def ConvertToBytes(self, string):
        return bytes(string, 'UTF-8') #converting to bytes

    # Convert bytes receieved to string
    def ConvertToString(self, inc_bytes):
        return str(inc_bytes, 'UTF-8').strip('\r\n')

    def ClearReadQueue(self):
        self.read_Queue.clear()

    def ClearSendQueue(self):
        self.send_Queue.clear()

    def __del__(self):
        try:
            #self.p.send_signal(SIGINT) #sending interupt signals to python script to close serial
            self.socket_listener.join() #ending daemon listener thread
            self.p.send_signal(CTRL_C_EVENT) #sending interupt signals to python script to close serial, change to UNIX SIGINT in future
            self.p.terminate() #may need to do p.kill()
            self.conn.close() #close socket
            log.debug('Deleting Serial Communciator Class')
        except:
            log.error('Failure to close Serial Communicator Class properly')
