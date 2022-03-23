# testing uart directly versus using serial communicator

from Util.UART_Serial_class import UART_Serial
from time import sleep
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

ser = UART_Serial()
ser.Open_Port('COM4')
ser.Write_Data("\r\n\r\n")
sleep(2)
ser.ser.flushInput()

ser.Write_Data('$H\n')

is_ok = ser.Read_Data()
while is_ok != 'ok':
    is_ok = ser.Read_Data()

print('taking pics or whatever...')
sleep(10)

ser.Write_Data('G90X-10\n')

is_ok = ser.Read_Data()
while is_ok != 'ok':
    is_ok = ser.Read_Data()

print('taking pics or whatever...')
sleep(10)

ser.Write_Data('G90X-20\n')

is_ok = ser.Read_Data()
while is_ok != 'ok':
    is_ok = ser.Read_Data()

print('taking pics or whatever...')
sleep(10)

ser.Write_Data('$H\n')

is_ok = ser.Read_Data()
while is_ok != 'ok':
    is_ok = ser.Read_Data()