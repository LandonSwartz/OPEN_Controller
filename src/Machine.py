#practice machine class for communicating with GUI
import os
from datetime import datetime
from time import sleep

from Util.Event import Event_Obj
from Util.GRBL_Arduino import GRBL_Arduino
#from Util.Vimba_Camera_Class import Vimba_Camera
from Util.Lights_Arduino import Lights_Arduino

import threading #for threading things

class Machine:

    #Class Variables - constants

    #commands for machine moving
    commands: dict = {1: 'G90X10', #first number is position number, next is grbl coorindate
                      2: 'G90X20',
                      3: 'G90X30'}

    #cameraSettingsPath: string
    #saveFolderPath: string
    #timelapse_interval: int
    #timelapse_end_date: datetime

    #Events for communicating with GUI
    OnGRBLConnected = Event_Obj()
    OffGRBLConnected = Event_Obj()
    OnLightConnected = Event_Obj()
    OffLightConnected = Event_Obj()
    OnCameraSettingsLoaded = Event_Obj()
    OffCameraSettingsLoaded = Event_Obj()

    def __init__(self):
        print('Machine class is initiated')

        #initating arduinos and camera
        self.grbl_ar = GRBL_Arduino('/dev/ttyACM0') #GRBL arduino
        #self.lights_ar = Lights_Arduino('portname')
        #self.camera = Vimba_Camera()

        self.saveFolderPath = None
        self.cameraSettingsPath = None
        self.timelapse_interval = None
        self.timelapse_end_date = None
        self.current_Position = None #current position'''

    def SetSaveFolderPath(self, path):
        # setting path
        self.saveFolderPath = path
        print("save folder setting path is {}".format(self.saveFolderPath))
        #print('save folder path is {}'.format(self.saveFolderPath))

        #make folders in save folder path
        if path: #if real path
            for position in self.commands:
                folder_name = "Position_" + str(position)
                folder_path = os.path.join(self.saveFolderPath, folder_name)
                try:
                    os.makedirs(folder_path)
                except OSError:
                    pass # pass if already exist

    def SetCameraSettingsPath(self, path):
        self.cameraSettingsPath = path

    def SetTimelapseInterval(self, interval):
        self.timelapse_interval = interval

    #Function that moves to specific location
    def MoveTo(self, posNum):
        print("Moving to position {}".format(posNum))
        self.grbl_ar.Send_Serial(self.commands[posNum]) #sending command

    def CaptureImage(self):
        print('Capturing image on vimba camera')
        self.camera.CaptureFrame()

    # TODO make sure this works
    def Filepath_Set(self, position_number):
        current_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        filename = current_time + '_' + position_number
        folder_name = "Position_" + position_number
        folder_path = os.path.join(self.saveFolderPath, folder_name)
        filepath = os.path.join(folder_path, filename)
        return filepath

    #Set Current Position, may not need
    def SetCurrentPosition(self, posNum):
        self.current_Position = posNum
        print("current_position is {}".format(self.current_Position))

    #Single Cycle Function, may throw into thread
    def SingleCycle(self):
        self.cycle_running = True
        self.stop_event = threading.Event()
        if self.cycle_running is True:
            self.cycle_thread = threading.Thread(target=self.SingleCycleThread)
            self.cycle_thread.start()
        self.cycle_thread.join() #wait until done, may not need

    def SingleCycleThread(self):
        wait = None

        #iterate through each position
        for position in self.commands:
            #move to position
            self.grbl_ar.Send_Serial(self.commands[position])
            #wait until at position
            while wait is None:
                wait = self.grbl_ar.Read_Serial()
                sleep(0.1)
            sleep(0.5)
            #capture image
            frame = self.camera.CaptureFrame()
            #make filepath and save image
            filepath = self.Filepath_Set(self.commands.get(position)) #check that this creates right things
            self.camera.SaveImage(frame, filepath)

    #Stops Single Cycle Function
    def StopCycle(self):
        print('stopping cycle')
        if self.cycle_thread.is_alive():
            self.stop_event.set() #setting stop event

    #Starts Timelapse
    def StartTimelapse(self):
        print('Start timelapse')
        self.grbl_ar.Send_Serial('$H\n')

    #Stops Timelapse
    def StopTimelapse(self):
        print("Stop timelapse")

    #event handling
    def AddSubscribersForOnConnectedGRBLEvent(self, objMethod):
        self.OnGRBLConnected += objMethod

    def AddSubscrubersForOffConnectedGRBLEvent(self, objMethod):
        self.OffGRBLConnected += objMethod

    def AddSubscribersForOnLightConnectedEvent(self, objMethod):
        self.OnLightConnected += objMethod

    def AddSubscriberForOffLightConnectedEvent(self, objMethod):
        self.OffLightConnected += objMethod

    def AddSubscribersForOnLoadCameraSettingsEvent(self, objMethod):
        self.OnCameraSettingsLoaded += objMethod

    def AddSubscriberForOffLoadCameraSettingsEvent(self, objMethod):
        self.OffCameraSettingsLoaded += objMethod

    def __del__(self):
        self.grbl_ar.__del__()
        self.lights_ar.__del__()
        self.camera.__del__() #may not need to delete

