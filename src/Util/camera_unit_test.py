# testing for camera module for OPEN Controller
# 4/6/2022

from Vimba_Camera_Class import Vimba_Camera
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

cam = Vimba_Camera()
sleep(0.5)

frame = cam.CaptureFrame()
sleep(0.5)

cam.SaveImage(frame, 'test.png')
sleep(0.5)

print('exiting tset program')

