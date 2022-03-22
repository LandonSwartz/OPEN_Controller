# serial communicator test


from Util.Serial_Communicator_Class import Serial_Communicator
from time import sleep
import sys
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

ser_com = Serial_Communicator('COM4', '50080')

sleep(1)

ser_com.ClearReadQueue()

#ser_com.Send('$H\n')

ser_com.Send('$H\n')

is_ok = ser_com.Read()
while is_ok != 'ok':
    is_ok = ser_com.Read()
    sleep(0.1)

print('Finished!')

sleep(1)

ser_com.__del__()

#print(ser_com.Read())

