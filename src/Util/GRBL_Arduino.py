# GRBL Subclass of Arduino class

#from src.Util.Arduino_Class import Arduino
#from src.Util.File_Class import File

from Arduino_Class import Arduino
from File_Class import File

class GRBL_Arduino(Arduino):

    # Dictionary of positions
    commands = {'Pos1': 10,
                'Pos2': 20,
                'Pos3': 30,
                'Pos4': 40}
    GRBL_Settings = File('Setting_Files/GRBL_settings.txt')

    def __init__(self, portname):
        #super().__init__()
        super(GRBL_Arduino, self).__init__(portname)
        self.SetGRBLSettings()

    # set GRBL Settings to serial port
    def SetGRBLSettings(self):
        #print('Send GRBL Settings')
        print('loading settings')
        #for line in self.GRBL_Settings.ReturnFileAsList():
            #print(line)
        for line in self.GRBL_Settings.ReturnFileAsList():
            self.Send_Serial(line)

    '''def SingleCycle(self): # May put into machine class
        wait = None

        for command in self.commands:
            self.ser.Send(command)
            while wait is None: #wait until receiving serial response of ok with GRBL command
                wait = self.ser.Read()
            wait = None # reset wait flag'''

    def HomeCommand(self):
        self.ser.Send('$H')

