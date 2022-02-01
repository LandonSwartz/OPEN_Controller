#main window application

import tkinter as tk
from src.GUI.Frames.Timelapse_Frame import TimelapseFrame
from src.GUI.Frames.Single_Cycle_Frame import SingleCycle
from src.GUI.Frames.Status_Frame import StatusFrame
from src.GUI.Frames.Title_Frame import Title
from src.GUI.Frames.Manual_Control_Frame import ManualControlFrame
#from src.Machine import Machine

#main frame
class MainApplication(tk.Frame):

    #machine = Machine

    def __init__(self, parent, Machine):
        tk.Frame.__init__(self)
        self.machine = Machine

        Title(parent).grid(row=0, column=0)
        StatusFrame(self, self.machine).grid(row=1, column=0)
        SingleCycle(self, self.machine).grid(row=2, column=0)
        TimelapseFrame(self, self.machine).grid(row=3, column=0)
        ManualControlFrame(self, self.machine).grid(row=4, column=0)