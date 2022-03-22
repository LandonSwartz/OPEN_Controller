# grbl testing arduino

from src.Util.GRBL_Arduino import GRBL_Arduino
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

grbl_ar = GRBL_Arduino('COM4')
sleep(1)
#grbl_ar.HomeCommand()
grbl_ar.Send_Serial('$X')
sleep(1)

is_ok = grbl_ar.Read_Serial()
while is_ok != 'ok':
    is_ok = grbl_ar.Read_Serial()
    sleep(0.1)

sleep(3)

grbl_ar.Send_Serial('G90X-10\r\n')

is_ok = grbl_ar.Read_Serial()
while is_ok != 'ok':
    is_ok = grbl_ar.Read_Serial()
    sleep(0.1)