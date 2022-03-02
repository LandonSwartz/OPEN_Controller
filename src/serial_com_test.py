# serial communicator test

from Util.Serial_Communicator_Class import Serial_Communicator
from time import sleep

ser_com = Serial_Communicator('COM1', '60000')
ser_com2 = Serial_Communicator('COM2', '50000')
sleep(3)
read = ser_com.Read()
read2 = ser_com2.Read()
print("Ser_com1 recieved: " + read)
print("Ser_com2 received: " + read)

