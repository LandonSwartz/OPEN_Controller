#practice machine class for communicating with GUI
import logging
import os
from time import sleep
from Util.Event import Event_Obj
from Util.GRBL_Arduino import GRBL_Arduino
#from Util.Vimba_Camera_Class import Vimba_Camera
from Util.Lights_Arduino import Lights_Arduino
from Util.File_Class import File
import time
import schedule
from datetime import datetime, time

import threading #for threading things

logger = logging.getLogger('open_controller_log.log')


class Machine:

    # Class Variables - constants

    # command list
    grbl_commands = File('Setting_Files/grbl_commands.txt')
    start_of_night = 22
    end_of_night = 7

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
        # print('Machine class is initiated')
        self.stop_event = None
        logger.info('Machine class is initiated')

        #initating arduinos and camera
        self.grbl_ar = GRBL_Arduino('COM4') #GRBL arduino
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
        logger.debug('save folder setting path is {}'.format(self.saveFolderPath))
        commands = self.grbl_commands.ReturnFileAsList()

        #make folders in save folder path
        if path: #if real path
            for position in commands:
                folder_name = "Position_" + str(commands.index(position)) #this should return the number, may need to add 1 as well
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
        #print("Moving to position {}".format(posNum))
        logger.info('Moving to position {}'.format(posNum))
        self.grbl_ar.Send_Serial(self.commands[posNum]) #sending command

    def CaptureImage(self):
        # print('Capturing image on vimba camera')
        logger.info('Capturing image on vimba camera')
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
        # print("current_position is {}".format(self.current_Position))
        logger.debug('Current Position is {}'.format(self.current_Position))

    #Single Cycle Function, may throw into thread
    def SingleCycle(self):
        self.cycle_running = True
        current_time = time.time()
        morning_time = "07:00:00"
        morning_time = time.strftime(morning_time)
        evening_time = "22:00:00"

        # check if night time and return cancel job
        if self.in_between(datetime.now().time(),
                           time(self.start_of_night),
                           time(self.end_of_night)):
            return schedule.CancelJob # cancel job because its nighttime

        if self.cycle_running is True:
            cycle_thread = threading.Thread(target=self.SingleCycleThread)
            cycle_thread.start()
            cycle_thread.join() #wait until done, may not need
            cycle_thread = None

        self.cycle_running = False

    def SingleCycleThread(self):
        commands = self.grbl_commands.ReturnFileAsList()

        #iterate through each position
        for position in commands:
        #move to position
            if self.cycle_running is True:
                self.grbl_ar.Send_Serial(position)
                #wait until at position
                sleep(5)
                #capture image
                #frame = self.camera.CaptureFrame()
                #make filepath and save image
                #filepath = self.Filepath_Set(self.commands.get(position)) #check that this creates right things
                #self.camera.SaveImage(frame, filepath)
            else:
                pass

    # Sees if time is between two ppints, useful for determining nighttime
    def in_between(self, now, start, end):
        if start <= end:
            return start <= now < end
        else:  # over midnight e.g., 23:30-04:15
            return start <= now or now < end

    #Stops Single Cycle Function, TODO: figure out how to stop later
    def StopCycle(self):
        logging.info('stopping single cycle thread')
        self.cycle_running = False # finish last move then joining thread

    #Starts Timelapse
    def StartTimelapse(self):
        logging.info('Starting timelapse')
        self.timelapse_running = True

        if self.timelapse_running is True:
            timelapse_thread = threading.Thread(target=self.TimelapseThread)
            timelapse_thread.start()
            timelapse_thread.join()  # wait until done, may not need

        self.timelapse_running = False

    def TimelapseThread(self):
        current_date = time.time()

        schedule.every(self.timelapse_interval).hour.until(self.timelapse_end_date).do(self.SingleCycle) #can change and set schedule with this using GUI!

        while self.timelapse_end_date - current_date > 0 and self.timelapse_running is True:
            schedule.run_pending()
            sleep(1)
            logging.debug('waiting... {} secs left'.format(round(self.timelapse_end_date - current_date)))
            current_date = time.time()

    #Stops Timelapse
    def StopTimelapse(self):
        logging.info('Stopping timelapse')
        self.timelapse_running = False

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
        #self.lights_ar.__del__()
        #self.camera.__del__() #may not need to delete

