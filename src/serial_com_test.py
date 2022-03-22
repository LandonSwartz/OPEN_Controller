# serial communicator test


from Util.Serial_Communicator_Class import Serial_Communicator
from time import sleep
import sys
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

ser_com = Serial_Communicator('COM4', '50080')

sleep(5)

#ser_com.Send('$H\n')

ser_com.Send('$H\n')

sleep(5)

while True:
    pass

#print(ser_com.Read())

