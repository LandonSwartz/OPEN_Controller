from multiprocessing.connection import Listener
import subprocess
from time import sleep

def main():
    #server
    adr = ('localhost', 6000)

    with Listener(adr, authkey=b'password') as listener:
        with listener.accept() as conn:
            print('connection accepted from', listener.last_accepted)

            while True:
                conn.send_bytes(b'testing')
                sleep(1)
                print(conn.recv_bytes())
                sleep(1)


if __name__ == '__main__':
    p = subprocess.Popen(['python', 'client.py'], shell=True)
    print('pid', p.pid)
    main()
