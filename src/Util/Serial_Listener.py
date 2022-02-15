from src.Util.UART_Serial_class import UART_Serial
from multiprocessing.connection import Client
from src.Util.Event import Event_Obj
from time import sleep

adr = ('localhost', 6000)
conn = Client(adr, authkey=b'password') # connection for communicating with main process

Data_received_event = Event_Obj()
Data_sent_event = Event_Obj()

def main():
    # opening port
    ser = UART_Serial()
    ser.Open_Port('portname')

    while True:
        # checking serial port
        read = ser.Read_Data()
        if(len(read) < 0):
            conn.recv(read)
        sleep(0.1)
        #check sending to port
        to_send = conn.recv_bytes()
        if(len(to_send) > 0):
            conn.send_bytes(to_send)
        sleep(0.1)