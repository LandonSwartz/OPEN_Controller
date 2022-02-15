from Util.UART_Serial_class import UART_Serial
from time import sleep

ser = UART_Serial()
ser.Open_Port('/dev/ttyACM0')
ser.Flush_Port()

sleep(1)

while(1):
    serial_read = ser.Read_Data()
    sleep(.5)
    if serial_read:
        ser.Write_Data('?')
        sleep(0.5)