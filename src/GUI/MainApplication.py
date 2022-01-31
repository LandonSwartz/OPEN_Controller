#main application

import tkinter as tk
from Frames.TimelapseFrame import TimelapseFrame
from Frames.SingleCycle_frame import SingleCycle
from Frames.StatusFrame import StatusFrame
from Frames.TitleFrame import Title
from Frames.ManualControlFrame import ManualControlFrame
from src.Machine import Machine

#main frame
class MainApplication(tk.Frame):

    #machine = Machine()

    def __init__(self, parent, Machine):
        tk.Frame.__init__(self)
        self.machine = Machine

        Title(parent).grid(row=0, column=0)
        StatusFrame(self, self.machine).grid(row=1, column=0)
        SingleCycle(self, self.machine).grid(row=2, column=0)
        TimelapseFrame(self, self.machine).grid(row=3, column=0)
        ManualControlFrame(self, self.machine).grid(row=4, column=0)