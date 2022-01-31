#practice machine class for communicating with GUI

from Util.UART_Serial import UART_Serial

class Machine:

    numPos: int = [1, 2, 3, 4, 5, 6, 7] #number of positions of machine
    GRBL_Positions = [0, 10, 20, 30, 40, 50, 60] #GRBL coordinates for sending to command
    #ser = serial.Serial('dev/ttyUSB0') #open serial port
    #ser = UART_Serial('portname') #change name

    def __init__(self):
        print('Machine class is initated')

    def singleCycle(self):
        for pos in self.numPos:
            print('Position {} executed'.format(pos))

    def openSerial(self):
        ser = serial.Serial('/dev/ttyUSB0') #opening serial port
        #double checking name in the future