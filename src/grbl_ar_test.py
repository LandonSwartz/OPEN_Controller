# grbl testing arduino

from src.Util.GRBL_Arduino import GRBL_Arduino
import logging
from time import sleep
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

grbl_ar = GRBL_Arduino('COM4')
sleep(2)

grbl_ar.SingleCycleTest()

'''grbl_ar.SendCommand('G90X-10')
print('taking pics...')
sleep(5)
grbl_ar.SendCommand('G90X-20')
print('taking pics...')
sleep(5)
grbl_ar.SendCommand('G90X-30')
print('taking pics...')
sleep(5)
grbl_ar.HomeCommand()

grbl_ar.__del__()'''

