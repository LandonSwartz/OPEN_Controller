#GRBL Subclass of Arduino class

from src.Util.Arduino_Class import Arduino
#Don't know if this anything
class GRBL_Arduino(Arduino):

    commandQueue = [] #Queue of Commands

    def __init__(self, portname):
        #super().__init__()
        super(GRBL_Arduino, self).__init__(portname)

    #move single cycles to here?