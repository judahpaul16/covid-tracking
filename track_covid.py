from PIL import Image, ImageTk
from itertools import count
from tkinter import *
import tkinter as tk
from tkinter import simpledialog as tk_input
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
import sqlite3	
import pandas as pd
from datetime import date
import urllib.request
import subprocess
import pathlib
import base64
import time
import os
import sys
import csv
import re

class MainDialog(tk_input.Dialog): # Overwritten
    # organize the layout of the input box
    def body(self, master):
        self.winfo_toplevel().title("COVID Tracking With GNUPlot")

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
        graph_type = str(self.e2.get())
        self.result = state, graph_type
        if state == '' or graph_type == '':
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

def plot(graph_type):

	if graph_type == 1:
		with open('data.csv', 'r') as file:
			os.system(f"gnuplot -e \"num_lines={sum(1 for line in file)}\" gnuplot_cumm.gp")

	elif graph_type == 2:
		with open('data.csv', 'r') as file:
			os.system(f"gnuplot -e \"num_lines={sum(1 for line in file)}\" gnuplot_noncumm.gp")

def main():
	
	try:    
	    # initialize input variables
		state = ''
		graph_type = ''
		graph_file = ''
		# state definitions
		state_to_abbrev = {
			'Alabama': 'AL',
			'Alaska': 'AK',
			'American Samoa': 'AS',
			'Arizona': 'AZ',
			'Arkansas': 'AR',
			'California': 'CA',
			'Colorado': 'CO',
			'Connecticut': 'CT',
			'Delaware': 'DE',
			'District of Columbia': 'DC',
			'Florida': 'FL',
			'Georgia': 'GA',
			'Guam': 'GU',
			'Hawaii': 'HI',
			'Idaho': 'ID',
			'Illinois': 'IL',
			'Indiana': 'IN',
			'Iowa': 'IA',
			'Kansas': 'KS',
			'Kentucky': 'KY',
			'Louisiana': 'LA',
			'Maine': 'ME',
			'Maryland': 'MD',
			'Massachusetts': 'MA',
			'Michigan': 'MI',
			'Minnesota': 'MN',
			'Mississippi': 'MS',
			'Missouri': 'MO',
			'Montana': 'MT',
			'Nebraska': 'NE',
			'Nevada': 'NV',
			'New Hampshire': 'NH',
			'New Jersey': 'NJ',
			'New Mexico': 'NM',
			'New York': 'NY',
			'North Carolina': 'NC',
			'North Dakota': 'ND',
			'Northern Mariana Islands':'MP',
			'Ohio': 'OH',
			'Oklahoma': 'OK',
			'Oregon': 'OR',
			'Pennsylvania': 'PA',
			'Puerto Rico': 'PR',
			'Rhode Island': 'RI',
			'South Carolina': 'SC',
			'South Dakota': 'SD',
			'Tennessee': 'TN',
			'Texas': 'TX',
			'Utah': 'UT',
			'Vermont': 'VT',
			'Virgin Islands': 'VI',
			'Virginia': 'VA',
			'Washington': 'WA',
			'West Virginia': 'WV',
			'Wisconsin': 'WI',
			'Wyoming': 'WY'
		}

		abbrev_to_state = dict(map(reversed, state_to_abbrev.items()))

		# download data files
		response_us = str(urllib.request.urlopen('https://github.com/nytimes/covid-19-data/raw/master/us.csv').read())
		lines = str(response_us).strip("b'").split("\\n")
		with open('raw_us_data.csv', 'w') as file:
			for line in lines:
				file.write(line + "\n")

		response_states = str(urllib.request.urlopen('https://github.com/nytimes/covid-19-data/raw/master/us-states.csv').read())
		lines = str(response_states).strip("b'").split("\\n")
		with open('raw_states_data.csv', 'w') as file:
			for line in lines:
				file.write(line + "\n")

		response_ny_curve = str(urllib.request.urlopen('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/archive/case-hosp-death.csv').read())
		lines = str(response_ny_curve).strip("b'").replace("\\r", "").split("\\n")
		with open('ny_curve.csv', 'w') as file:
			for line in lines:
				file.write(line + "\n")

		# get user input from dialog
		try:
			state = window.result[0].replace(' ', '')
			graph_type = window.result[1].replace(' ', '')
		except TypeError:
			pass

		# end program upon hitting 'Cancel' or [X]
		if state == '' or graph_type == '':
			root.destroy()
			raise SystemExit

		if state != "NY" and graph_type == "2":
			tkMessageBox.showwarning('Information Not Available',
				'Unfortunately, Non-cummulative data is only available for New York at this time. Please try again.')

		elif state == "NY" and graph_type == "2":
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			os.rename('ny_curve.csv', 'data.csv')
			plot(2)

		elif state != "US" and graph_type == "1":
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			df = pd.read_csv('raw_states_data.csv')
			df.drop(df.index[df['state'] != abbrev_to_state[state]], inplace=True)
			df.drop('state', axis=1, inplace=True)
			df.drop('fips', axis=1, inplace=True)
			df.to_csv('data.csv', index=False)
			plot(1)

		elif state == "US" and graph_type == "1":
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			os.rename('raw_us_data.csv','data.csv')
			plot(1)

		tkMessageBox.showinfo("Success", "GIF Successfully Generated!")

	except:
		tkMessageBox.showerror("Error", "GIF Generation Failed. Please Try Again.")

if __name__ == '__main__':
	# popup tkinter input dialog
	root = Tk()
	center(root)
	root.update()
	root.withdraw()
	window = MainDialog(root)
	# get the graph
	main()