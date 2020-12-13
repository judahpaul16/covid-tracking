from tkinter import *
import tkinter as tk
from tkinter import simpledialog as tk_input
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
import pandas as pd
from datetime import date
import urllib.request
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
    master.geometry(f'{width}x{height}+{x}+{y}')
    master.resizable(False, False)
    master.deiconify()

def download_csv(response, filename):

	lines = str(response).strip("b'").replace("\\r", "").split("\\n")
	with open(filename, 'w') as file:
		for line in lines:
			file.write(line + "\n")

def plot(graph_type, state_full):

	if graph_type == 1:
		with open('data.csv', 'r') as file:
			os.system(f"gnuplot -e \"num_lines={sum(1 for line in file)}\" \
								-e \"state=\'{state_full.upper()}\'\" gnuplot_cumm.gp")

	elif graph_type == 2 and state_full == "New York":
		with open('data.csv', 'r') as file:
			os.system(f"gnuplot -e \"num_lines={sum(1 for line in file)}\" \
								-e \"state=\'{state_full.upper()}\'\" gnuplot_ny_noncumm.gp")

	elif graph_type == 2:
		with open('data.csv', 'r') as file:
			os.system(f"gnuplot -e \"num_lines={sum(1 for line in file)}\" \
								-e \"state=\'{state_full.upper()}\'\" gnuplot_noncumm.gp")

def main():
	
	try:    
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

		# get user input from dialog
		try:
			state = window.result[0].replace(' ', '').upper()
			graph_type = window.result[1].replace(' ', '')
		except TypeError:
			pass

		# end program upon hitting 'Cancel' or [X]
		if state == '' or graph_type == '':
			root.destroy()
			raise SystemExit
		
		if state != "US" and graph_type == "1":
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			df = pd.read_csv('raw_states_data.csv')
			df.drop(df.index[df['state'] != abbrev_to_state[state]], inplace=True)
			df.drop('state', axis=1, inplace=True)
			df.drop('fips', axis=1, inplace=True)
			df.to_csv('data.csv', index=False)
			plot(1, abbrev_to_state[state])

		elif state == "US" and graph_type == "1":
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			shutil.copy2('raw_us_data.csv', 'data.csv')
			plot(1, abbrev_to_state[state])

		elif state == "US" and graph_type == "2":
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
			plot(2, abbrev_to_state[state])

		elif state == "NY" and graph_type == "2":
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			shutil.copy2('ny_curve.csv', 'data.csv')
			plot(2, abbrev_to_state[state])

		elif (state != "NY" and state != "US") and graph_type == "2":
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
			plot(2, abbrev_to_state[state])

		tkMessageBox.showinfo("Success", "GIF Successfully Generated!")

		if graph_type == 1: os.startfile('graph_cumm.gif')
		elif graph_type == 2: os.startfile('graph_noncumm.gif')

	except Exception as e:
		tkMessageBox.showerror("Error", f"GIF Generation Failed. Please Try Again.\n\nMore Info: {e}")


if __name__ == '__main__':
	# popup tkinter input dialog
	root = Tk()
	center(root)
	root.update()
	root.withdraw()
	window = MainDialog(root)
	# get the graph
	main()