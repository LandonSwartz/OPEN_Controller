#client socket

import socket
from time import sleep

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.settimeout(0.1)
    sleep(0.1)
    s.sendall(b'Hello Server! from client')

    while True:
        #recieve data, check socket then send data from socket also
        try:
            data = s.recv(1024)
            if data:
                data_string = str(data, 'UTF-8')
                print("client received: " + data_string)
        except socket.timeout: #instead of TimeoutError
            #print('no data in client')
            pass

        sleep(0.1)

        #send data (check serial and do nothing if nothing)
        '''try:
            #s.send(b'hello from client')
            sleep(0.1)
        except TimeoutError:
            print('not able to send from client')
        sleep(0.1)

        sleep(0.1)'''
