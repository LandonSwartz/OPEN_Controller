#server socket for testing timeout

import subprocess
import socket
from time import sleep

HOST = "127.0.0.1" #standard loopback interface address (localhost)
PORT = 65432 #Port to listen on

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(1) #setting timeout
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            #while True:
            '''#receiving data
                try:
                    data = conn.recv(1024)
                    if data: #if data exist
                        print('From server :')
                        print(data)
                        print('\n')
                except TimeoutError:
                    print('no data from clients')
                sleep(0.1)

                #send data
                try:
                    conn.sendall(b'server hello')
                    sleep(0.1)
                except TimeoutError:
                    print('server timeout sending')'''

            try:
                data = conn.recv(1024)
                data_string = str(data, 'UTF-8')
                print('server received: ' + data_string)
                conn.send(b'first message')
                sleep(1)
                conn.send(b'second message')
                sleep(3)
                conn.send(b'last message')
                sleep(1)
            except TimeoutError:
                print('server timeout sending')

if __name__ == '__main__':
    p = subprocess.Popen(['python', 'socket_client.py'], shell=True)
    print('pid', p.pid)
    sleep(0.5)
    main()