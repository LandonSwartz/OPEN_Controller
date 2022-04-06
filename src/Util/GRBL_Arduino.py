# GRBL Subclass of Arduino class

#from src.Util.Arduino_Class import Arduino
#from src.Util.File_Class import File

#from Util.Arduino_Class import Arduino
import logging

from Util.Arduino_Class import Arduino
from Util.File_Class import File
from time import sleep


class GRBL_Arduino(Arduino):

    #GRBL_Settings = File('Setting_Files/GRBL_settings.txt')
    #GRBL_Commands = File('Setting_Files/grbl_commands.txt') # may not be able to use

    def __init__(self, portname):
        super(GRBL_Arduino, self).__init__(portname)
        self.ser_port.Write_Data("\r\n\r\n") # wake up grbl
        sleep(2)
        self.ser_port.ser.flushInput()        # flush input messages
        self.HomeCommand()

    def SingleCycleTest(self):
        single_cycle_commands = self.GRBL_Commands.ReturnFileAsList()

        for command in single_cycle_commands:
            self.SendCommand(command)
            sleep(4)

    # homing commands wait until we have ok signal, other manual commands go to ok right away
    def SendCommand(self, command):
        try:
            self.Send_Serial(command + '\n')
            sleep(0.5)
            is_ok = self.ser_port.Read_Data()
            while is_ok != 'ok':
                is_ok = self.ser_port.Read_Data()
                #logging.debug('is_ ok is {}'.format(is_ok))
            sleep(0.1)
            self.ser_port.ser.flushInput()
        except:
            return False

    # set GRBL Settings to serial port
    def SetGRBLSettings(self):
        #print('Send GRBL Settings')
        print('loading settings')
        #for line in self.GRBL_Settings.ReturnFileAsList():
            #print(line)
        for line in self.GRBL_Settings.ReturnFileAsList():
            self.Send_Serial(line)

    def HomeCommand(self):
        self.SendCommand('$H\n')
        #self.Send_Serial('$H\n')
