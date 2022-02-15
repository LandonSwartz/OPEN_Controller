#practice machine class for communicating with GUI
import string
from datetime import datetime

from Util.UART_Serial_class import UART_Serial
from Util.Event import Event_Obj
from Util.GRBL_Arduino import GRBL_Arduino
from Util.Vimba_Camera_Class import Vimba_Camera

#TODO -implement communicating with serial, -connect with lights and GRBL, - move function

class Machine:

    #Class Variables
    numPos: int = (1, 2, 3, 4, 5, 6, 7) #number of positions of machine
    GRBL_Positions: int = [0, 10, 20, 30, 40, 50, 60] #GRBL coordinates for sending to command
    current_Position: int
    #ser = serial.Serial('dev/ttyUSB0') #open serial port
    #ser = UART_Serial('portname') #change name

    cameraSettingsPath: string
    saveFolderPath: string
    timelapse_interval: int
    timelapse_end_date: datetime

    grbl_arduino = GRBL_Arduino('/dev/ttyACM0')
    vimba_camera = Vimba_Camera()

    #Events
    OnGRBLConnected = Event_Obj()
    OffGRBLConnected = Event_Obj()
    OnLightConnected = Event_Obj()
    OffLightConnected = Event_Obj()
    OnCameraSettingsLoaded = Event_Obj()
    OffCameraSettingsLoaded = Event_Obj()

    def __init__(self):
        print('Machine class is initiated')

    def SetSaveFolderPath(self, path):
        self.saveFolderPath = path
        print("save folder setting path is {}".format(self.saveFolderPath))
        #print('save folder path is {}'.format(self.saveFolderPath))

    def SetCameraSettingsPath(self, path):
        self.cameraSettingsPath = path

    def SetTimelapseInterval(self, interval):
        self.timelapse_interval = interval

    #Function that moves to specific location
    def MoveTo(self, posNum):
        print("Moving to position {}".format(posNum))

    def CaptureImage(self):
        print('Capturing image on vimba camera')

    #Set Current Position, may not need
    '''def SetCurrentPosition(self, posNum):
        self.current_Position = posNum
        print("current_position is {}".format(self.current_Position))
        #log for current position'''

    #Single Cycle Function
    def SingleCycle(self):
        for pos in self.numPos:
            print('Position {} executed'.format(pos))

    #Stops Single Cycle Function
    def StopCycle(self):
        print('stopping cycle')

    #Starts Timelapse
    def StartTimelapse(self):
        print('Start timelapse')

    #Stops Timelapse
    def StopTimelapse(self):
        print("Stop timelapse")

    #Connection to Ardunios
    def Connect(self):
        #connect to lights and GRBL arduino
        print('connected')
        #self.OnGRBLConnected()

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

