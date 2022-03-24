# testing light arduino

from Util.Lights_Arduino import Lights_Arduino
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

lights_ar = Lights_Arduino("COM5")

sleep(10)

lights_ar.BackLightsOn()
lights_ar.GrowlightsOn()

sleep(2)