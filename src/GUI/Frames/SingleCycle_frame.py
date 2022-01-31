#single cycle control frames

import tkinter as tk
from tkinter import *
from tkinter import ttk

#for single cycle section
from Machine import Machine


class SingleCycle(tk.Frame, Machine):

    #machine = Machine

    #init
    def __init__(self, parent, Machine):
        tk.Frame.__init__(self)
        self.machine = Machine

        Single_cycle_label = tk.Label(self, text='Single Cycle').grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.Start_button = tk.Button(self, text='Start', command=self.startButton)
        self.Start_button.grid(row=1, column=0, padx=5, pady=5, ipadx=30, ipady=5, sticky='ew')

        self.Stop_Button = tk.Button(self, text='Stop', command=self.stopButton)
        self.Stop_Button.grid(row=1, column=1, padx=5, pady=5, ipadx=30, ipady=5, sticky='ew')

    def startButton(self):
        print('start')
        self.machine.singleCycle()
        #start single cycle

    def stopButton(self):
        print('stop')
        #stop cycle
