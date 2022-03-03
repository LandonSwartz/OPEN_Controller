#Lights Arduino Subclass

from Util.Arduino_Class import Arduino
from Util.UART_Serial_class import UART_Serial

#TODO - fill out commands

class Lights_Arduino(Arduino):

    backlight_state: bool = False
    growlight_state: bool = False
    
    def __init__(self, portname):
        super(Lights_Arduino, self).__init__(portname)
        #clearing on startup the lights
        self.AllOff()

    ###Combined Functions###

    #Turns on all of lights
    def AllOn(self):
        self.BackLightsOn()
        self.GrowlightsOn()

    #Turns off all lights
    def AllOff(self):
        self.BackLightsOff()
        self.GrowlightsOff()

    ###Manually Functions###

    #turning on Backlights when called with command
    def BackLightsOn(self):
        self.ser.Write_Data('S1V2') #or whatever command is
        self.backlight_state = True

    def BackLightsOff(self):
        self.ser.Write_Data('')
        self.backlight_state = False

    def GrowlightsOn(self):
        self.ser.Write_Data('')
        self.growlight_state = True

    def GrowlightsOff(self):
        self.ser.Write_Data('')
        self.growlight_state = False

    #Encapsulation Functions
    def GetBackLightStatus(self):
        return self.backlight_state

    def SetBackLightStatus(self, state: bool):
        self.backlight_state = state

    def GetGrowlightStatus(self):
        return self.growlight_state

    def SetGrowlightStatus(self, state: bool):
        self.growlight_state = state

