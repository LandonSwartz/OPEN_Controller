#status frame class

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os
from src.Util.Event import Event_Obj

#status of connections and others
class StatusFrame(tk.Frame):

    OnSaveFolderPathChange = Event_Obj()

    #init
    def __init__(self, parent, Machine):
        # Status Frame
        tk.Frame.__init__(self)

        self.machine = Machine

        #have to declare after tk.Frame
        red_light = ImageTk.PhotoImage(Image.open('GUI/assets/red_light.png'))

        GRBL_connection = tk.Label(self, text="GRBL Connection:").grid(row=1, column=1, pady=5, padx=5, sticky='w')

        self.GRBL_status_graphic = tk.Label(self, image=red_light)
        self.GRBL_status_graphic.image = red_light
        self.GRBL_status_graphic.grid(row=1, column=2, pady=5, padx=5)
        #self.GRBL_status_graphic.bind('<Enter>', self.UpdateStatus('<Enter>', self.GRBL_status_graphic))

        Lights_connection = tk.Label(self, text='Lights Connection:').grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.Lights_status_graphic = tk.Label(self, image=red_light)
        self.Lights_status_graphic.image = red_light
        self.Lights_status_graphic.grid(row=1, column=4, padx=5, pady=5)
        #self.Lights_status_graphic.bind('<Enter>', self.UpdateStatus('<Enter>', self.Lights_status_graphic))

        Camera_Setting_status = tk.Label(self, text='Camera Status:').grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.Camera_setting_graphic = tk.Label(self, image=red_light)
        self.Camera_setting_graphic.image = red_light
        self.Camera_setting_graphic.grid(row=2, column=2, padx=5, pady=5)
        #self.Camera_setting_graphic.bind('<Enter>', self.UpdateStatus('<Enter>', self.Camera_setting_graphic))

        Save_Folder_Label = tk.Label(self, text='Save Folder Location:').grid(row=3, column=1, padx=5, pady=5)
        self.Save_Folder_Textbox = tk.Text(self, height=1, width=20, font=('Arial', 12))
        self.Save_Folder_Textbox.grid(row=3, column=2, columnspan=2, pady=5, sticky='ew') #.grid returns none so must separate if editing
        Save_Folder_Button = tk.Button(self, text='Click', command=self.browseFiles).grid(row=3,column=4, padx=5, pady=5, ipadx=5)

    # Function for opening the
    # file explorer window
    def browseFiles(self, event=None):
        # creating path to save folder
        filename = filedialog.askdirectory(initialdir="/", title="Select a File")
        if filename:
            filepath: str = os.path.abspath(filename)
        # setting to class' save location settings

        # Change textbox contents
        self.Save_Folder_Textbox.delete('1.0', END) #to clear textbox, needs 1.0 for line 1 and char 0
        self.Save_Folder_Textbox.insert('1.0', str(filepath)) #refill textbox

        self.OnSaveFolderPathChange(filepath)

    #Check status of GRBL Connection on event of GRBL connected in machine
    def ChangeGRBLStatusOn(self):
        green_light = ImageTk.PhotoImage(Image.open('GUI/assets/green_light.png'))
        self.GRBL_status_graphic.configure(image=green_light)
        self.GRBL_status_graphic.image = green_light
        print("GRBL Status Graphic changed")

    #Change image of GRBL connection on event of GRBL connection not working
    def ChangeGRBLStatusOff(self):
        red_light = ImageTk.PhotoImage(Image.open('GUI/assets/red_light.png'))
        self.GRBL_status_graphic.configure(image=red_light)
        self.GRBL_status_graphic.image=red_light

    #Change image of Lights Arduino graphic on event of machine connecting to Ardunio
    def ChangeLightsStatusOn(self):
        green_light = ImageTk.PhotoImage(Image.open('GUI/assets/green_light.png'))
        self.Lights_status_graphic.configure(image=green_light)
        self.Lights_status_graphic.image = green_light
        print("Lights Status Graphic changed")

    #Change lights Ardunio Connection to off graphic on event of disconnection in machine
    def ChangeLightsStatusOff(self):
        red_light = ImageTk.PhotoImage(Image.open('GUI/assets/red_light.png'))
        self.Lights_status_graphic.configure(image=red_light)
        self.Lights_status_graphic.image=red_light

    #Change Camera Settings Loaded Graphic to on graphic on event of load settings in machine
    def ChangeCameraSettingsOn(self):
        green_light = ImageTk.PhotoImage(Image.open('GUI/assets/green_light.png'))
        self.Camera_setting_graphic.configure(image=green_light)
        self.Camera_setting_graphic.image = green_light

    #Changes Camera Settings Loaded Graphic to off graphic on event of not load settings in machine
    def ChangeCameraSettingsOff(self):
        red_light = ImageTk.PhotoImage(Image.open('GUI/assets/red_light.png'))
        self.Camera_setting_graphic.configure(image=red_light)
        self.Camera_setting_graphic.image=red_light

    def AddSubscriberSaveFolderPathChanged(self, objMethod):
        self.OnSaveFolderPathChange += objMethod
