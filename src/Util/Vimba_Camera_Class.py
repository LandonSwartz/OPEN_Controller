# Class wrapper for Vimba Camera to facilate easier use

import os.path

import cv2
from vimba import *
from datetime import datetime

class Vimba_Camera(object):

    vimba_ins = Vimba.get_instance()
    settings_file = 'src/Setting_Files/camera_settings.xml' #TODO set this constant

    def __init__(self):
        self.save_location = None
        self.camera = self.Connect() # because only one cam should be attached
     #   self.save_location = saveLocation #file path to save folder location

    def Connect(self):
        cams = self.vimba_ins.get_all_cameras()
        return cams[0] #returns only instance of all cameras

    def SetSaveLocation(self, save_location_path):
        self.save_location = save_location_path #pass folder path for save location

    def LoadSettings(self):
        self.camera.load_settings(self.settings_file, PersistType.All)

    #gets and return Frame already converted
    def CaptureFrame(self, posNum):
        if(self.save_location):
            frame = self.camera.get_frame()
            frame.convert_pixel_format(PixelFormat.BayerGB12)
            self.SaveImage(frame, posNum)
            return frame # may not return
        else:
            print("No Save Location Set")

    def SaveImage(self, frame, posNum):
        filename = self.Filepath_Create(posNum)
        cv2.imwrite(filename, frame.as_opencv_image())

    def Filepath_Set(self, position_number):
        current_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        filename = current_time + '_' + position_number
        filepath = os.path.join(self.save_location, filename)
        return filepath

