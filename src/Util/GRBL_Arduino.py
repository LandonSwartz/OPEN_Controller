# GRBL Subclass of Arduino class

from src.Util.Arduino_Class import Arduino
from src.Util.File_Class import File
#Don't know if this anything
class GRBL_Arduino(Arduino):

    commandQueue = [] #Queue of Commands
    GRBL_Settings = File('setting.txt')

    def __init__(self, portname):
        #super().__init__()
        super(GRBL_Arduino, self).__init__(portname)
        self.SetGRBLSettings()

    # set GRBL Settings
    def SetGRBLSettings(self):
        print('Send GRBL Settings')
        for line in self.GRBL_Settings.ReturnFileAsList():
            print(line)