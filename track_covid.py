from state_dict import abbrev_to_state, state_to_abbrev
from spinner import Spinner
from dialog import MainDialog, center_window
from tkinter import Tk, messagebox
import pandas as pd
from datetime import date
from urllib.request import urlopen
import traceback
import pathlib
import base64
import shutil
import time
import os
import sys
import csv

def download_csv(url, filename):
	response = str(urlopen(url).read())
	lines = str(response).strip("b'").replace("\\r", "").split("\\n")
	with open(filename, 'w') as file:
		for line in lines:
			file.write(line + "\n")

def generate_gif(graph_type, state):
	# declare variables
	the_void = '' 	# a place for gnuplot warning messages to be sent
	num_lines = ''	# number of lines of plot data
	cases = ''		# plot data for graph legend
	deaths = '' 	# plot data for graph legend
	hosp = ''		# plot data for graph legend

	# if Operating System is Windows
	if os.name == 'nt':
		the_void = "> NUL 2>&1"
	# otherwise this should work for Linux and MacOS
	else:
		the_void = "2>/dev/null"

	df = pd.read_csv('data.csv') # pandas dataframe with plot data
	with open('data.csv', 'r') as file:
		num_lines = sum(1 for line in file)

	# decision tree to plot
	if graph_type == 1:
		for item in df['cases']: cases += (' ' + str(item))
		for item in df['deaths']: deaths += (' ' + str(item))
		os.system(f"gnuplot -e \"num_lines={num_lines}\" \
							-e \"cases = \'{cases}\'\" \
							-e \"deaths = \'{deaths}\'\" \
							-e \"state=\'{state.upper()}\'\" gnuplot_cumm.gp {the_void}")

	elif graph_type == 2 and state == "New York":
		for item in df['CASE_COUNT']: cases += (' ' + str(item))
		for item in df['DEATH_COUNT']: deaths += (' ' + str(item))
		for item in df['HOSPITALIZED_COUNT']: hosp += (' ' + str(item))
		os.system(f"gnuplot -e \"num_lines={num_lines}\" \
							-e \"cases = \'{cases}\'\" \
							-e \"deaths = \'{deaths}\'\" \
							-e \"hosp = \'{hosp}\'\" \
							-e \"state=\'{state.upper()}\'\" gnuplot_ny_noncumm.gp {the_void}")

	elif graph_type == 2:
		for item in df['cases']: cases += (' ' + str(int(item)))
		for item in df['deaths']: deaths += (' ' + str(int(item)))
		os.system(f"gnuplot -e \"num_lines={num_lines}\" \
							-e \"cases = \'{cases}\'\" \
							-e \"deaths = \'{deaths}\'\" \
							-e \"state=\'{state.upper()}\'\" gnuplot_noncumm.gp {the_void}")

def display_gif(gif_file):
	# if Operating System is Windows
	if os.name == 'nt':
		os.startfile(gif_file)
	# otherwise this should work for Linux and MacOS
	else:
		os.system(f'xviewer {gif_file}')

def Exit():
	root.destroy()
	raise SystemExit

# decorator function for displaying the program's runtime
def timer(original_func):
	def wrapper(*args, **kwargs):
		t1 = time.time()
		result = original_func(*args, **kwargs)
		t2 = time.time() - t1
		print(f'\n\n[Finished in {t2} sec]')
		return result
	return wrapper

@timer
def main():
    # declare variables
	abbrev = '' 		# user input: state abbreviation (i.e. 'NY')
	graph_type = ''		# user input: '1' for cummulative, '2' for noncummulative
	gif_file = ''		# filename for the output gif

	try:
		# get user input from dialog window
		try:
			abbrev = input_box.result[0].replace(' ', '').upper()
			graph_type = input_box.result[1]
		except TypeError:
			pass

		# end program upon hitting 'Cancel' or [X]
		if abbrev == '' or (graph_type != 1 and graph_type != 2):
			root.destroy()
			raise SystemExit
		
		# decision tree to generate the GIF
		if abbrev != "US" and graph_type == 1:
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			gif_file = 'graph_cumm.gif'
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'
			filename = 'raw_states_data.csv'
			download_csv(url, filename)
			df = pd.read_csv(filename)
			df.drop(df.index[df['state'] != abbrev_to_state[abbrev]], inplace=True)
			df.drop('state', axis=1, inplace=True)
			df.drop('fips', axis=1, inplace=True)
			df.to_csv('data.csv', index=False)

			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(1, abbrev_to_state[abbrev])

		elif abbrev == "US" and graph_type == 1:
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			gif_file = 'graph_cumm.gif'
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us.csv'
			filename = 'raw_us_data.csv'
			download_csv(url, filename)
			shutil.copy2(filename, 'data.csv')

			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(1, abbrev_to_state[abbrev])

		elif abbrev == "US" and graph_type == 2:
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			gif_file = 'graph_noncumm.gif'
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us.csv'
			filename = 'raw_us_data.csv'
			download_csv(url, filename)
			df_1 = pd.read_csv(filename)
			df_2 = df_1.loc[:,['cases', 'deaths']].diff() # cummulative --> noncummulative
			df_1.drop(['cases', 'deaths'], axis=1, inplace=True)
			df_merged = pd.concat([df_1, df_2], axis=1)
			df_merged.dropna(inplace=True)
			df_merged.astype({"cases":'int', "deaths":'int'})
			df_merged.to_csv('data.csv', index=False)

			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(2, abbrev_to_state[abbrev])

		elif abbrev == "NY" and graph_type == 2:
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			gif_file = 'graph_noncumm.gif'
			url = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/archive/case-hosp-death.csv'
			filename = 'ny_curve.csv'
			download_csv(url, filename)
			shutil.copy2(filename, 'data.csv')

			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(2, abbrev_to_state[abbrev])

		elif abbrev != "US" and graph_type == 2:
			try:
				os.remove('data.csv')
			except FileNotFoundError:
				pass

			gif_file = 'graph_noncumm.gif'
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'
			filename = 'raw_states_data.csv'
			download_csv(url, filename)
			df_1 = pd.read_csv(filename)
			df_1.drop(df_1.index[df_1['state'] != abbrev_to_state[abbrev]], inplace=True)
			df_1.drop('state', axis=1, inplace=True)
			df_1.drop('fips', axis=1, inplace=True)
			df_2 = df_1.loc[:,['cases', 'deaths']].diff() # cummulative --> noncummulative
			df_1.drop(['cases', 'deaths'], axis=1, inplace=True)
			df_merged = pd.concat([df_1, df_2], axis=1)
			df_merged.dropna(inplace=True)
			df_merged.astype({"cases":'int', "deaths":'int'})
			df_merged.to_csv('data.csv', index=False)

			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(2, abbrev_to_state[abbrev])

		messagebox.showinfo("Success", "GIF Successfully Generated!")

		# popup the GIF
		display_gif(gif_file)

	except Exception as e:
		messagebox.showerror("Error: GIF Generation Failed.", f"More Information:\n\n{traceback.format_exc()}")

if __name__ == '__main__':
	# popup tkinter input dialog
	root = Tk()
	center_window(root)
	root.update()
	root.withdraw()
	input_box = MainDialog(root)
	
	main()