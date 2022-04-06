# Class wrapper for Vimba Camera to facilate easier use
import logging
import os.path

import cv2
from vimba import *
from datetime import datetime

log = logging.getLogger('open_controller_log.log')

'''Using with statement throughout this class to grab and autodelete vimba camera.
    The instance still persist.'''

class Vimba_Camera(object):

    #vimba_ins = Vimba.get_instance()
    settings_file = 'src/Setting_Files/camera_settings.xml' #TODO set this constant

    def __init__(self):
        log.debug('Vimba Camera Class initiated')
        self.save_location = None
        #self.LoadSettings()
     #   self.save_location = saveLocation #file path to save folder location

    #def SetSaveLocation(self, save_location_path):
        #self.save_location = save_location_path #pass folder path for save location

    def LoadSettings(self):
        with Vimba.get_instance() as vimba_ins:  
            cams = vimba_ins.get_all_cameras()
            with cams[0] as cam:
                cam.load_settings(self.settings_file, PersistType.All)

    def CaptureImage(self, filepath):
        frame = self.CaptureFrame()
        self.SaveImage(frame, filepath)

    #gets and return Frame already converted
    def CaptureFrame(self):
        with Vimba.get_instance() as vimba_ins: 
            cams = vimba_ins.get_all_cameras()
            with cams[0] as cam:
                # converting to Bayer Format
                cam.set_pixel_format(PixelFormat.BayerGR12)
                #Capturing frame
                frame = cam.get_frame()
                log.info('Image Captured with vimba camera')
                return frame  # may not return

    def SaveImage(self, frame, filename):
        #get the raw image as numpy array from frame
        image = frame.as_numpy_ndarray()
        #use opencv to convert from raw Bayer to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #write image to disk
        cv2.imwrite(filename, rgb_image)
        log.info('Image writen to disk at {}'.format(filename))

    def __del__(self):
        log.debug('Vimba Camera class deleted')
