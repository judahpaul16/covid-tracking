from tkinter import *
import tkinter as tk
from tkinter import simpledialog as tk_input
import tkinter.messagebox as messagebox
import pandas as pd
from datetime import date
import urllib.request
import traceback
import itertools
import threading
import pathlib
import base64
import shutil
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
        Label(master, text="\"1\" for Cummulative, \"2\" for Non-cummulative", font=('Roboto', 8)).grid(row=5, column=1)

        self.e1 = Entry(master, textvariable=StringVar())
        self.e2 = Entry(master, textvariable=StringVar())

        self.e1.grid(row=2, column=1, sticky='we')
        self.e2.grid(row=4, column=1, sticky='we')
        return self.e1 # initial focus

    # Overwritten: this executes upon hitting 'Okay'
    def validate(self):
        state = str(self.e1.get())
        graph_type = int(self.e2.get())
        self.result = state, graph_type
        if state == '' or (graph_type != 1 and graph_type != 2):
            return 0
        else:
            return 1

class Spinner: # credit to Ruslan Dautkhanov --> https://github.com/Tagar/stuff/blob/master/spinner.py

    def __init__(self, message, delay=0.1):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.delay = delay
        self.busy = False
        self.spinner_visible = False
        sys.stdout.write(message)

    def write_next(self):
        with self._screen_lock:
            if not self.spinner_visible:
                sys.stdout.write(next(self.spinner))
                self.spinner_visible = True
                sys.stdout.flush()

    def remove_spinner(self, cleanup=False):
        with self._screen_lock:
            if self.spinner_visible:
                sys.stdout.write('\b')
                self.spinner_visible = False
                if cleanup:
                    sys.stdout.write(' ')
                    sys.stdout.write('\r')
                sys.stdout.flush()

    def spinner_task(self):
        while self.busy:
            self.write_next()
            time.sleep(self.delay)
            self.remove_spinner()

    def __enter__(self):
        if sys.stdout.isatty():
            self._screen_lock = threading.Lock()
            self.busy = True
            self.thread = threading.Thread(target=self.spinner_task)
            self.thread.start()

    def __exit__(self, exception, value, tb):
        if sys.stdout.isatty():
            self.busy = False
            self.remove_spinner(cleanup=True)
        else:
            sys.stdout.write('\r')

# centers a tkinter window
def center_window(master):

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
    master.geometry(f'{width}x{height}+{x}+{y}')
    master.resizable(False, False)
    master.deiconify()

def download_csv(response, filename):

	lines = str(response).strip("b'").replace("\\r", "").split("\\n")
	with open(filename, 'w') as file:
		for line in lines:
			file.write(line + "\n")

def generate_gif(graph_type, state_full):

	the_void = '' # a place for gnuplot warning messages to be sent
	num_lines = ''
	cases = ''
	deaths = ''
	hosp = ''
	df = pd.read_csv('data.csv')

	# initialize variables
	if os.name == 'nt': # if OS is Windows
		the_void = "> NUL 2>&1"
	else:
		the_void = "2>/dev/null"

	with open('data.csv', 'r') as file:
		num_lines = sum(1 for line in file)

	if graph_type == 1:
		for item in df['cases']: cases += (' ' + str(item))
		for item in df['deaths']: deaths += (' ' + str(item))
		os.system(f"gnuplot -e \"num_lines={num_lines}\" \
							-e \"cases = \'{cases}\'\" \
							-e \"deaths = \'{deaths}\'\" \
							-e \"state=\'{state_full.upper()}\'\" gnuplot_cumm.gp {the_void}")

	elif graph_type == 2 and state_full == "New York":
		for item in df['CASE_COUNT']: cases += (' ' + str(item))
		for item in df['DEATH_COUNT']: deaths += (' ' + str(item))
		for item in df['HOSPITALIZED_COUNT']: hosp += (' ' + str(item))
		os.system(f"gnuplot -e \"num_lines={num_lines}\" \
							-e \"cases = \'{cases}\'\" \
							-e \"deaths = \'{deaths}\'\" \
							-e \"hosp = \'{hosp}\'\" \
							-e \"state=\'{state_full.upper()}\'\" gnuplot_ny_noncumm.gp {the_void}")

	elif graph_type == 2:
		for item in df['cases']: cases += (' ' + str(int(item)))
		for item in df['deaths']: deaths += (' ' + str(int(item)))
		os.system(f"gnuplot -e \"num_lines={num_lines}\" \
							-e \"cases = \'{cases}\'\" \
							-e \"deaths = \'{deaths}\'\" \
							-e \"state=\'{state_full.upper()}\'\" gnuplot_noncumm.gp {the_void}")

def display_gif(graph_file):

	if os.name == 'nt': # if OS is Windows
		os.startfile(graph_file)
	else:
		os.system(f'xviewer {graph_file}')

def Exit():

	root.destroy()
	raise SystemExit

def main():
	 
    # initialize input variables
	state = ''
	graph_type = ''
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
		'United States' : 'US',
		'Vermont': 'VT',
		'Virgin Islands': 'VI',
		'Virginia': 'VA',
		'Washington': 'WA',
		'West Virginia': 'WV',
		'Wisconsin': 'WI',
		'Wyoming': 'WY'
	}

	abbrev_to_state = dict(map(reversed, state_to_abbrev.items()))

	try:
		# download data files
		response_us = str(urllib.request.urlopen('https://github.com/nytimes/covid-19-data/raw/master/us.csv').read())
		filename = 'raw_us_data.csv'
		download_csv(response_us, filename)

		response_states = str(urllib.request.urlopen('https://github.com/nytimes/covid-19-data/raw/master/us-states.csv').read())
		filename = 'raw_states_data.csv'
		download_csv(response_states, filename)

		response_ny_curve = str(urllib.request.urlopen('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/archive/case-hosp-death.csv').read())
		filename = 'ny_curve.csv'
		download_csv(response_ny_curve, filename)

		# get user input from dialog window
		try:
			state = window.result[0].replace(' ', '').upper()
			graph_type = window.result[1]
		except TypeError:
			pass

		# end program upon hitting 'Cancel' or [X]
		if state == '' or (graph_type != 1 and graph_type != 2):
			root.destroy()
			raise SystemExit
		
		if state != "US" and graph_type == 1:
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			df = pd.read_csv('raw_states_data.csv')
			df.drop(df.index[df['state'] != abbrev_to_state[state]], inplace=True)
			df.drop('state', axis=1, inplace=True)
			df.drop('fips', axis=1, inplace=True)
			df.to_csv('data.csv', index=False)
			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(1, abbrev_to_state[state])

		elif state == "US" and graph_type == 1:
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			shutil.copy2('raw_us_data.csv', 'data.csv')
			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(1, abbrev_to_state[state])

		elif state == "US" and graph_type == 2:
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			df_1 = pd.read_csv('raw_us_data.csv')
			df_2 = df_1.loc[:,['cases', 'deaths']].diff()
			df_1.drop(['cases', 'deaths'], axis=1, inplace=True)
			df_merged = pd.concat([df_1, df_2], axis=1)
			df_merged.dropna(inplace=True)
			df_merged.astype({"cases":'int', "deaths":'int'})
			df_merged.to_csv('data.csv', index=False)
			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(2, abbrev_to_state[state])

		elif state == "NY" and graph_type == 2:
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			shutil.copy2('ny_curve.csv', 'data.csv')
			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(2, abbrev_to_state[state])

		elif (state != "NY" and state != "US") and graph_type == 2:
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			df_1 = pd.read_csv('raw_states_data.csv')
			df_1.drop(df_1.index[df_1['state'] != abbrev_to_state[state]], inplace=True)
			df_1.drop('state', axis=1, inplace=True)
			df_1.drop('fips', axis=1, inplace=True)
			df_2 = df_1.loc[:,['cases', 'deaths']].diff()
			df_1.drop(['cases', 'deaths'], axis=1, inplace=True)
			df_merged = pd.concat([df_1, df_2], axis=1)
			df_merged.dropna(inplace=True)
			df_merged.astype({"cases":'int', "deaths":'int'})
			df_merged.to_csv('data.csv', index=False)
			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(2, abbrev_to_state[state])

		print() # formatting
		messagebox.showinfo("Success", "GIF Successfully Generated!")

		if graph_type == 1:
			display_gif('graph_cumm.gif')
		elif graph_type == 2:
			display_gif('graph_noncumm.gif')

	except Exception as e:
		messagebox.showerror("Error: GIF Generation Failed.", f"More Information:\n\n{traceback.format_exc()}")

if __name__ == '__main__':

	# popup tkinter input dialog
	root = Tk()
	center_window(root)
	root.update()
	root.withdraw()
	window = MainDialog(root)
	# begin analysis
	main()