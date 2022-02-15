from multiprocessing.connection import Client
import time
adr = ('localhost', 6000)

with Client(adr, authkey=b'password') as conn:
    while True:
        print(conn.recv_bytes())
        time.sleep(1)
        conn.send_bytes(b'sending back bytes')
        time.sleep(1)