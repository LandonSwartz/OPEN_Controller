# Class wrapper for Vimba Camera to facilate easier use
import logging
import os.path

import cv2
from vimba import *
from datetime import datetime

log = logging.getLogger('open_controller_log.log')

class Vimba_Camera(object):

    #vimba_ins = Vimba.get_instance()
    #settings_file = 'src/Setting_Files/camera_settings.xml' #TODO set this constant

    def __init__(self):
        log.debug('Vimba Camera Class initiated')
        self.save_location = None
        self.camera = self.Connect() # because only one cam should be attached
     #   self.save_location = saveLocation #file path to save folder location

    def Connect(self):
    	with Vimba.get_instance() as vimba_ins:
        	cams = vimba_ins.get_all_cameras()
        	return cams[0] #returns only instance of all cameras

    #def SetSaveLocation(self, save_location_path):
        #self.save_location = save_location_path #pass folder path for save location

    def LoadSettings(self):
        self.camera.load_settings(self.settings_file, PersistType.All)

    #gets and return Frame already converted
    def CaptureFrame(self):
    	with Vimba.get_instance() as vimba_ins: 
    		cams = vimba_ins.get_all_cameras()
    		with cams[0] as cam:
				frame = cam.get_frame()
				frame.convert_pixel_format(PixelFormat.BayerGB12)
				log.info('Image Captured with vimba camera')
				#self.SaveImage(frame)
				return frame  # may not return

    def SaveImage(self, frame, filename):
        cv2.imwrite(filename, frame.as_opencv_image())
        log.info('Image writen to disk at {}'.format(filename))

    def __del__(self):
        log.debug('Vimba Camera class deleted')
