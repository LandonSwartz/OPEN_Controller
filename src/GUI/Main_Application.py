#main window application

import tkinter as tk
from src.GUI.Frames.Timelapse_Frame import TimelapseFrame
from src.GUI.Frames.Single_Cycle_Frame import SingleCycle
from src.GUI.Frames.Status_Frame import StatusFrame
from src.GUI.Frames.Title_Frame import Title
from src.GUI.Frames.Manual_Control_Frame import ManualControlFrame
#from src.Machine import Machine
from time import sleep


#main frame
class MainApplication(tk.Frame):

    #machine = Machine
    def __init__(self, parent, Machine):
        tk.Frame.__init__(self)
        self.machine = Machine

        Title(parent).grid(row=0, column=0)
        self.status_frame = StatusFrame(self, self.machine)
        self.status_frame.grid(row=1, column=0)
        self.single_cycle = SingleCycle(self, self.machine)
        self.single_cycle.grid(row=2, column=0)
        self.timelapse_frame = TimelapseFrame(self, self.machine)
        self.timelapse_frame.grid(row=3, column=0)
        self.manual_control_frame = ManualControlFrame(self, self.machine)
        self.manual_control_frame.grid(row=4, column=0)

        #Event Handling Setting Subscribers#

        #single cycle
        self.single_cycle.AddSubscriberForOnSingleCycleEvent(self.machine.SingleCycle)
        self.single_cycle.AddSubscribersForOnStopSingleCycleEvent(self.machine.StopCycle)

        #status events
        self.machine.AddSubscribersForOnConnectedGRBLEvent(self.status_frame.ChangeGRBLStatusOn)
        self.machine.AddSubscrubersForOffConnectedGRBLEvent(self.status_frame.ChangeGRBLStatusOff)
        self.machine.AddSubscribersForOnLightConnectedEvent(self.status_frame.ChangeLightsStatusOn)
        self.machine.AddSubscriberForOffLightConnectedEvent(self.status_frame.ChangeLightsStatusOff)
        self.machine.AddSubscribersForOnLoadCameraSettingsEvent(self.status_frame.ChangeCameraSettingsOn)
        self.machine.AddSubscriberForOffLoadCameraSettingsEvent(self.status_frame.ChangeCameraSettingsOff())
        self.status_frame.AddSubscriberSaveFolderPathChanged(self.machine.SetSaveFolderPath)

        #manual frame events, will fill out in future when finish with machine
        #self.manual_control_frame.AddSubscriberForPositionNumChanged(self.machine.SetCurrentPosition)
        self.manual_control_frame.AddSubscriberForMoveToBtnPressed(self.machine.MoveTo)
        self.manual_control_frame.AddSubscriberForManualImageCaptureBtnPressed(self.machine.CaptureImage)
        #self.manual_control_frame.AddSubscriberForManualBacklightOnBtnPressed()
        #self.manual_control_frame.AddSubscriberForManualBacklightOffBtnPressed()
        #self.manual_control_frame.AddSubscriberForManualGrowlightOnBtnPressed()
        #self.manual_control_frame.AddSubscriberForManualGrowlightOffBtnPressed()
