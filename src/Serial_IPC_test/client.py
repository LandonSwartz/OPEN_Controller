from multiprocessing.connection import Client
from time import sleep
import os

adr = ('localhost', 6000)

with Client(address=adr, authkey=None) as conn:

    while True:
        print(conn.recv_bytes())
        sleep(1)
        conn.send_bytes(b'sending back bytes')
        sleep(1)