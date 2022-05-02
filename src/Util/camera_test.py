import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
from Vimba_Camera_Class import Vimba_Camera
from time import sleep

cam = Vimba_Camera()
sleep(2)
cam.LoadSettings()
sleep(2)
cam.CaptureFrame()