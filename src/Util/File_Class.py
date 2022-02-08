# File Utility Class

import string
import os

class File(object):

    current_working_dir = os.getcwd()

    def __init__(self, filename):
        filename_full = os.path.join(self.current_working_dir, filename)
        self.file_obj = self.OpenFileRead(filename_full)

    # Opens file with given filename
    def OpenFileRead(self, filename: string):
        try:
            return open(filename, 'r')
        except FileNotFoundError:
            print('Failed to open file')

    def OpenFileWrite(self, filename: string):
        try:
            return open(filename, 'w')
        except FileNotFoundError:
            print('Failed to open file')

    def IsClosed(self):
        return self.file_obj.closed() #True if closed, false otherwise

    def ReturnMode(self):
        return self.file_obj.mode()

    def ReturnName(self):
        return self.file_obj.name()

    # Return false if space explicivityly required with print, true otherwise
    def ReturnSoftspace(self):
        return self.file_obj.softspace()

    # Return file as list for iterating
    def ReturnFileAsList(self):
        lines = self.file_obj.readlines()
        return lines

    def __del__(self):
        self.file_obj.close()

