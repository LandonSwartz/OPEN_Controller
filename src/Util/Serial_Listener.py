#Serial listener process

from src.Util.UART_Serial_class import UART_Serial
from time import sleep
import socket
import sys

print('starting serial sub process')
sleep(0.1)

portname = sys.argv[1]
socket_port = sys.argv[2]
adr = ('127.0.0.1', int(socket_port))  # localhost on pi
ser = UART_Serial()
ser.Open_Port(portname)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(adr)
    s.settimeout(0.1)
    sleep(0.1)
    s.sendall(b'Hello Server! I am connected from serial client')

    try:
        #Event loop
        while True:
            #recieve data, check socket then send data from socket also
            try:
                data = s.recv(1024)

                if data:    #if recieved something from socket
                    data_string = str(data, 'UTF-8')
                    print("client received: " + data_string) #TODO change to log eventually
                    ser.Write_Data(data) #write to serial
            except socket.timeout: #instead of TimeoutError
                #print('no data in client')
                pass

            sleep(0.1)

            #send data (check serial and do nothing if nothing)
            try:
                ser_data = ser.Read_Data() #check to make sure in bytes
                if ser_data:
                    s.send(ser_data) #send recievd serial data over socket
                    ser_data_string = str(ser_data, 'UTF-8')
                    print('serial sent: ' + ser_data_string)
            except TimeoutError:
                # print('not able to send from client')
                pass

            sleep(0.1)
    except KeyboardInterrupt:
        ser.Close_Port()