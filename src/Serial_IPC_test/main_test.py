import os
from multiprocessing.connection import Listener
import subprocess
from time import sleep

def main():
    #server
    adr = ('localhost', 6000)

    with Listener(address=adr, authkey=None) as listener:
        with listener.accept() as conn:
            print('connection accepted from', listener.last_accepted)

            while True:
                conn.send_bytes(b'testing')
                sleep(1)
                #print('msg type is {}'.format(type(msg)))
                try:
                    print(conn.recv_bytes())
                except EOFError:
                    print('Nothing in pipe')
                sleep(1)

if __name__ == '__main__':
    p = subprocess.Popen(['python', 'client.py'], shell=True)
    print('pid', p.pid)
    sleep(1)
    main()
