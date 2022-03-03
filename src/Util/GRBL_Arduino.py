# GRBL Subclass of Arduino class

#from src.Util.Arduino_Class import Arduino
#from src.Util.File_Class import File

from Util.Arduino_Class import Arduino
from Util.File_Class import File

class GRBL_Arduino(Arduino):

    GRBL_Settings = File('Setting_Files/GRBL_settings.txt')

    def __init__(self, portname):
        #super().__init__()
        super(GRBL_Arduino, self).__init__(portname)
        self.HomeCommand()
        #self.SetGRBLSettings()

    # set GRBL Settings to serial port
    def SetGRBLSettings(self):
        #print('Send GRBL Settings')
        print('loading settings')
        #for line in self.GRBL_Settings.ReturnFileAsList():
            #print(line)
        for line in self.GRBL_Settings.ReturnFileAsList():
            self.Send_Serial(line)

    def HomeCommand(self):
        self.Send_Serial('$H\n')
