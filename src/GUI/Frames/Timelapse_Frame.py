#Timelapse frame for UI

import tkinter as tk
from tkinter import *
from tkinter import ttk

#for event handling
from src.Util.Event import Event_Obj

#TODO
#-implement the events for this frame


class TimelapseFrame(tk.Frame):

    #Will need to set default values for machine because only updates when changed

    #init
    def __init__(self, parent, Machine):
        tk.Frame.__init__(self)
        #self['bg']='red'      #finding messed up grid things
        #self.grid(sticky='ew')
        self.machine = Machine

        time_units = ('hours', 'days', 'weeks')
        decimal_units = ('1', '2', '3', '4', '5', '6', '7', '8', '9')

        #timelapse title
        Timelapse_title = tk.Label(self, text='Timelapse').grid(row=0, column=0, columnspan=6, sticky='EW')

        #interval
        Interval_title = tk.Label(self, text='Interval:').grid(row=1, column=0)

        self.Interval_combobox = ttk.Combobox(self, width=3, textvariable=tk.StringVar())
        self.Interval_combobox['values'] = decimal_units
        self.Interval_combobox['state'] = 'readonly'
        self.Interval_combobox.current(1)
        self.Interval_combobox.bind('<<ComboboxSelected>>', func=self.Interval_dec_set)
        self.Interval_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.Interval_combobox_time_unit = ttk.Combobox(self, width=5, textvariable=tk.StringVar())
        self.Interval_combobox_time_unit['values'] = time_units
        self.Interval_combobox_time_unit['state'] = 'readonly'
        self.Interval_combobox_time_unit.current(0)
        self.Interval_combobox_time_unit.bind('<<ComboboxSelected>>', func=self.Interval_time_unit_set)
        self.Interval_combobox_time_unit.grid(row=1, column=2, padx=5, pady=5)

        #end date
        End_date = tk.Label(self, text="End Date:").grid(row=1, column=3)

        self.End_date_dec = ttk.Combobox(self, width=3, textvariable=tk.StringVar())
        self.End_date_dec['values'] = decimal_units
        self.End_date_dec['state'] = 'readonly'
        self.End_date_dec.current(1)
        self.End_date_dec.bind('<<ComboboxSelected>>', func=self.End_date_interval_set)
        self.End_date_dec.grid(row=1, column=4, padx=5, pady=5)

        self.End_date_time = ttk.Combobox(self, width=5, textvariable=StringVar())
        self.End_date_time['values'] = time_units
        self.End_date_time['state'] = 'readonly'
        self.End_date_time.current(0)
        self.End_date_time.bind('<<ComboboxSelected>>', func=self.End_date_time_set)
        self.End_date_time.grid(row=1, column=5, padx=5, pady=5)

        #Start and Stop Button
        self.Start_Button = tk.Button(self, text='Start', command=self.Start_Button)
        self.Start_Button.grid(row=2, column=0, columnspan=3,
                               padx=5, ipadx=30, pady=5, ipady=5,
                               sticky='ew')

        self.Stop_Button = tk.Button(self, text='Stop', command=self.Stop_Button)
        self.Stop_Button.grid(row=2, column=3, columnspan=3,
                              padx=5, ipadx=30, pady=5, ipady=5,
                              sticky='ew')

    def Interval_dec_set(self, event):
        #set value of machine timelapse interval here
        print('The value of timelapse interval is: ' + self.Interval_combobox.get())

    def Interval_time_unit_set(self, event):
        #set time unit for timelapse
        print('Timelapse interval time unit is ' + self.Interval_combobox_time_unit.get())

    def End_date_interval_set(self, event):
        #set end date interval
        print('End Date interval is: ' + self.End_date_dec.get())

    def End_date_time_set(self, event):
        #setting time unit for end date
        print('End date time unit is: ' + self.End_date_time.get())

    def Start_Button(self):
        #starting timelapse
        print('Starting Cycle...')

    def Stop_Button(self):
        #stopping timelapse
        print('Stopping Cycle...')

