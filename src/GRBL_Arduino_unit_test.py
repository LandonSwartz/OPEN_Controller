#GRBL arduino unit test

from Util.UART_Serial_class import UART_Serial
from Util.GRBL_Arduino import GRBL_Arduino
from time import sleep

g_ar = GRBL_Arduino('/dev/ttyACM0')

sleep(0.5)

print(g_ar.serial.IsDataInSerial())

for x in range(10):
    g_ar.Read_Serial()
    sleep(.5)

sleep(1)

g_ar.Send_Serial('?')

sleep(3)

g_ar.Read_Serial()