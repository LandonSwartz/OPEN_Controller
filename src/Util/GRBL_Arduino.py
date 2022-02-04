#GRBL Subclass of Arduino class

from src.Util.Arduino_Class import Arduino

class GRBL_Arduino(Arduino):

    commandQueue = [] #Queue of Commands

    def __init__(self):
        #super().__init__()
        super(GRBL_Arduino, self).__init__()