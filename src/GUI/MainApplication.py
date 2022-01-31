#main application

import tkinter as tk
from GUI.Frames.TimelapseFrame import TimelapseFrame
from GUI.Frames.SingleCycle_frame import SingleCycle
from GUI.Frames.StatusFrame import StatusFrame
from GUI.Frames.TitleFrame import Title
from GUI.Frames.ManualControlFrame import ManualControlFrame
from Machine import Machine

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