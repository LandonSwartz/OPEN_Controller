#draft of OPEN Controller UI, actual design

import tkinter as tk
from GUI.Main_Application import MainApplication
from Machine import Machine

def main():
    #maindow set up
    root = tk.Tk()
    root.title("OPEN Controller")
    #root.geometry('800x600') #set window size
    #root.resizable(False, False) #turning off resizing

    machine = Machine()

    #classes for GUI
    app = MainApplication(root, machine)
    #try to put app into smaller window

    #run window
    app.mainloop()

if __name__ == '__main__':
    main()