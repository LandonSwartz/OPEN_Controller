#Lights Arduino Subclass

from Util.Arduino_Class import Arduino

#TODO - fill out commands

class Lights_Arduino(Arduino):

    backlight_state: bool = False
    growlight_state: bool = False
    
    def __init__(self, portname):
        super(Lights_Arduino, self).__init__(portname)

        # clearing on startup the lights
        self.AllOff()

    ### Combined Functions ###

    # Turns on all of lights
    def AllOn(self):
        self.BackLightsOn()
        self.GrowlightsOn()

    # Turns off all lights
    def AllOff(self):
        self.BackLightsOff()
        self.GrowlightsOff()

    ### Manually Functions ###

    # turning on Backlights when called with command
    def BackLightsOn(self):
        self.ser_port.Write_Data('S2V1\n') #or whatever command is
        self.backlight_state = True

    # Turns off Backlights when called
    def BackLightsOff(self):
        self.ser_port.Write_Data('S2V0\n')
        self.backlight_state = False

    # Turns on Growlight Relay signal on arduino
    def GrowlightsOn(self):
        self.ser_port.Write_Data('S1V1\n')
        self.growlight_state = True

    #Turns off Growlight Relay Signal on arduino
    def GrowlightsOff(self):
        self.ser_port.Write_Data('S1V0\n')
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

    # deleting method that turns off lights on way out
    def __del__(self):
        self.AllOff()

