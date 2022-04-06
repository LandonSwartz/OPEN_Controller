import time

from Machine_Class import Machine
from time import sleep
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

current_time = time.time()

machine = Machine()
machine.timelapse_end_date = current_time + (6*60)
sleep(0.5)

'''sleep(1)
machine.StartTimelapse()

sleep(10)'''

# camera testing
machine.CaptureImage('test.png')
