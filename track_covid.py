from tkinter import *
import tkinter as tk
from tkinter import simpledialog as tk_input
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
import sqlite3	
import pandas as pd
from datetime import date
import urllib.request
import os
import csv
import re

response_us = str(urllib.request.urlopen('https://github.com/nytimes/covid-19-data/raw/master/us.csv').read())
with open('raw_us_data.dat', 'w') as file:
	file.write(response_us)

response_states = str(urllib.request.urlopen('https://github.com/nytimes/covid-19-data/raw/master/us.csv').read())
with open('tmp.dat', 'w') as file:
	file.write(response_states)

response_ny_curve = str(urllib.request.urlopen('https://github.com/nytimes/covid-19-data/raw/master/us.csv').read())
with open('ny_curve.dat', 'w') as file:
	file.write(response_ny_curve)

class MainDialog(tk_input.Dialog): # Overwritten
    # organize the layout of the input box
    def body(self, master):
        self.winfo_toplevel().title("COVID Tracking")

        Label(master, text="Input Below the State Abbreviation and Graph\nType For Visualization",
            font=('Roboto', 12, 'bold')).grid(row=0, column=0, columnspan=2, rowspan=2)
        Label(master, text="", font=('Roboto', 12)).grid(row=1)
        Label(master, text="State   - - - - -> ", font=('Roboto', 10)).grid(row=2)
        Label(master, text="\"NY\" for New York, \"US\" for United States", font=('Roboto', 8)).grid(row=3, column=1)
        Label(master, text="Graph Type  - - - ->", font=('Roboto', 10)).grid(row=4)
        Label(master, text="Cummulative: \"1\" | Non-cummulative: \"2\"", font=('Roboto', 8)).grid(row=5, column=1)

        self.e1 = Entry(master, textvariable=StringVar())
        self.e2 = Entry(master, textvariable=StringVar())

        self.e1.grid(row=2, column=1, sticky='we')
        self.e2.grid(row=4, column=1, sticky='we')
        return self.e1 # initial focus

    # Overwritten: this executes upon hitting 'Okay'
    def validate(self):
        state = str(self.e1.get())
        gType = str(self.e2.get())
        self.result = state, gType
        if state == '' or gType == '':
            return 0
        else:
            return 1

# centers a tkinter window
def center(master):

    master.withdraw()
    master.update_idletasks()
    width = master.winfo_width()
    frm_width = master.winfo_rootx() - master.winfo_x()
    win_width = width + 3 * frm_width
    height = master.winfo_height()
    titlebar_height = master.winfo_rooty() - master.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = master.winfo_screenwidth() // 2 - win_width // 2
    y = master.winfo_screenheight() // 2 - win_height // 2
    master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    master.resizable(False, False)
    master.deiconify()

def main():

    # initialize input variables
    state = ''
    gType = ''

    # popup tkinter input box
    ROOT = tk.Tk()
    center(ROOT)
    ROOT.update()
    ROOT.withdraw()
    window = MainDialog(ROOT)

    # get user input
    try:
        state = window.result[0].replace(' ', '')
        gType = window.result[1].replace(' ', '')
    except TypeError:
        pass

    # end program upon hitting 'Cancel' or [X]
    if state == '' or gType == '':
        ROOT.destroy()
        raise SystemExit

    root.mainloop()

if __name__ == '__main__':
    main()