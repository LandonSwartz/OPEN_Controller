#title of program frame

import tkinter as tk

class Title(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        OC_title = tk.Label(self, text='OPEN Controller', justify='center',
                            font=('Arial', 22))
        OC_title.pack(fill='both', expand='true')
