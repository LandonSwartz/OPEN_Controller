#practice machine class for communicating with GUI
import logging
import os
from time import sleep
from Util.Event import Event_Obj
from Util.GRBL_Arduino import GRBL_Arduino
from Util.Vimba_Camera_Class import Vimba_Camera
from Util.Lights_Arduino import Lights_Arduino
from Util.File_Class import File
import time
import schedule
from datetime import datetime, date

import threading #for threading things

logger = logging.getLogger('open_controller_log.log')


class Machine:

    # Class Variables - constants
    
    # command list
    grbl_commands = File(os.path.join(os.getcwd(), 'src/Setting_Files/grbl_commands.txt'))
    #grbl_commands = File('/home/landon/Desktop/OPEN_Controller/src/Setting_Files/grbl_commands.txt')
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
        self.stop_event = None
        logger.info('Machine class is initiated')

        #initating arduinos and camera
        self.grbl_ar = GRBL_Arduino('/dev/ttyACM0') #GRBL arduino, plugged in first
        self.lights_ar = Lights_Arduino('/dev/ttyACM1') #plugged in second
        self.camera = Vimba_Camera()

        self.saveFolderPath = None
        self.cameraSettingsPath = None
        self.timelapse_interval = 2
        self.timelapse_end_date = date.today()
        self.current_Position = None
        self.timelapse_start_of_night = None
        self.timelapse_end_of_night = None

    def SetSaveFolderPath(self, path):
        # setting path
        self.saveFolderPath = path
        logger.debug('save folder setting path is {}'.format(self.saveFolderPath))
        commands = self.grbl_commands.ReturnFileAsList()
        #removing homing signals
        commands = commands[1:-1]
        
        #make folders in save folder path
        if path:    # if real path
            for position in commands:
                folder_name = "Position_" + str(commands.index(position)) #this should return the number, may need to add 1 as well
                folder_path = os.path.join(self.saveFolderPath, folder_name)
                try:
                    if not os.path.isdir(folder_path): # if folder not made then make it
                        os.makedirs(folder_path)
                        logger.debug('Folder made at {}'.format(folder_path))
                except OSError:
                    logger.error('Fialure to make folder {}'.format(folder_path))
                    pass # pass if already exist
                
        return

    def SetCameraSettingsPath(self, path):
        self.cameraSettingsPath = path

    def SetTimelapseInterval(self, interval):
        logger.debug("Timelapse interval is set to: {}".format(interval))
        self.timelapse_interval = int(interval)
        
    def SetTimelapseEndDate(self, end_date):
        end_date_datetime = datetime.combine(end_date, datetime.max.time())
        logger.debug("Timelapse end date is set to: {}".format(end_date_datetime))
        self.timelapse_end_date = end_date_datetime
        
    def SetTimelapseStartOfNight(self, start_of_night):
        logger.debug("Timelapse start of night is set to: {}".format(start_of_night))
        self.timelapse_start_of_night = start_of_night
        
    def SetTimelapseEndOfNight(self, end_of_night):
        end_of_night_datetime = datetime.strptime(end_of_night, '%Y-%m-%d %H:%M:%S')
        logger.debug("Timelapse end of night is set to: {}".format(end_of_night_datetime))
        self.timelapse_end_of_night = end_of_night_datetime

    # Function that moves to specific location
    # TODO fix move to bug, stops only after doiconvert string to datetime in pythonng it once
    def MoveTo(self, posNum):
        commands = self.grbl_commands.ReturnFileAsList()
        logger.info('Moving to position {}'.format(posNum))
        # sending command
        self.grbl_ar.Send_Serial(commands[int(posNum)])

    def CaptureImage(self, filepath):
        logger.info('Capturing image on vimba camera')
        self.camera.CaptureImage(filepath)

    # TODO make sure this works
    def Filepath_Set(self, position_number):
        current_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        filename = current_time + '_' + str(position_number) + '.png'
        folder_name = "Position_" + str(position_number)
        folder_path = os.path.join(self.saveFolderPath, folder_name)
        filepath = os.path.join(folder_path, filename)
        return filepath

    #Set Current Position, may not need
    def SetCurrentPosition(self, posNum):
        self.current_Position = posNum
        logger.debug('Current Position is {}'.format(self.current_Position))

    #Single Cycle Function, may throw into thread
    def SingleCycle(self):
        self.cycle_running = True
        morning_time = "10:00:00"
        morning_time = datetime.strptime(morning_time, '%I:%M:%S') # from time library
        evening_time = "11:40:00"
        evening_time = datetime.strptime(evening_time, '%I:%M:%S')

        # check if night time and pass if it is
        if self.in_between(datetime.now().time(),
                           morning_time.time(),
                           evening_time.time()):
            logger.debug('It is nighttime')
        else: # it is not nighttime
            if self.cycle_running is True:
                cycle_thread = threading.Thread(target=self.SingleCycleThread)
                cycle_thread.start()
                cycle_thread.join() #wait until done, may not need
                cycle_thread = None

        self.cycle_running = False

    def SingleCycleThread(self):
        logger.debug('single cycle thread is running')
        commands = self.grbl_commands.ReturnFileAsList()
        self.lights_ar.GrowlightsOff()
        self.lights_ar.BackLightsOn()
        
        first_command = commands[0] # slicing first command off (ususally homing)
        commands = commands[1:]
        self.grbl_ar.Send_Serial(first_command)
        sleep(3)

        #iterate through each position
        for position in commands:
        #move to position
            if self.cycle_running is True:
                self.grbl_ar.Send_Serial(position)
                if not 'H' in position: #if not homing command
                    #wait until at position
                    sleep(5)
                    filepath = self.Filepath_Set(commands.index(position)) #check that this creates right things #TODO MAKE SURE WORK
                    self.camera.CaptureImage(filepath)
            else:
                pass
            
        self.lights_ar.GrowlightsOn()
        self.lights_ar.BackLightsOff()

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
                    #starting cycle
            self.SingleCycle()
        
            current_date = datetime.now()

            schedule.every(self.timelapse_interval).minutes.until(self.timelapse_end_date).do(self.SingleCycle) #can change and set schedule with this using GUI!

            self.stop_run_continously = self.run_continuously()
            
            # don't think need to make thread still since running in background now
            #timelapse_thread = threading.Thread(target=self.TimelapseThread)
            #timelapse_thread.start()
            #timelapse_thread.join()  # wait until done, may not need

        self.timelapse_running = False
        #timelapse_thread.join()  # wait until done, may not need

    def TimelapseThread(self):
        
        #starting cycle
        self.SingleCycle()
        
        current_date = datetime.now()

        schedule.every(self.timelapse_interval).minutes.until(self.timelapse_end_date).do(self.SingleCycle) #can change and set schedule with this using GUI!

        self.stop_run_continously = self.run_continuously()
            
    # example from schedule library website
    # link: https://schedule.readthedocs.io/en/stable/background-execution.html
    def run_continuously(self, interval=1):
        """Continuously run, while executing pending jobs at each
        elapsed time interval.
        @return cease_continuous_run: threading. Event which can
        be set to cease continuous run. Please note that it is
        *intended behavior that run_continuously() does not run
        missed jobs*. For example, if you've registered a job that
        should run every minute and you set a continuous run
        interval of one hour then your job won't be run 60 times
        at each interval but only once.
        """
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run
            
    def TimeToWait():
        counter = 60;
        start = time.time()
        
        while True:
            if time.time() - start > 1:
                start = time.time()
                counter = counter - 1
            
                log.debug("{} seconds remaining".format(counter))
            
                if counter <= 0:
                    break

    #Stops Timelapse
    def StopTimelapse(self):
        logging.info('Stopping timelapse')
        self.stop_run_continuously.set() #stopping continous run thread
        #self.timelapse_running = False
    
    def BackLights_On(self):
        logging.debug('Turning backlights on from machine class')
        self.lights_ar.BackLightsOn()
    
    def BackLights_Off(self):
        logging.debug('Turning backlights off from machine class')
        self.lights_ar.BackLightsOff()
        
    def GrowLights_On(self):
        logging.debug('Turning growlights on from machine class')
        self.lights_ar.GrowlightsOn()
        
    def GrowLights_Off(self):
        logging.debug('Turning growlights off from machine class')
        self.lights_ar.GrowlightsOff()

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

