# ------------------ LOCAL MODULES --------------------
from state_dict import abbrev_to_state, state_to_abbrev
from dialog import InputDialog, center_window
from spinner import Spinner
# ----------------- BULT-IN MODULES -------------------
from tkinter import Tk, Toplevel, messagebox
import traceback
import shutil
import time
import sys
import csv
import glob
import os
# ----------------- EXTERNAL MODULES ------------------
from urllib3 import PoolManager
from datetime import date
import pandas as pd
import pathlib

# popup tkinter input dialog
root = Tk()
center_window(root)
root.update()
root.withdraw()
input_box = InputDialog(root)
root.wm_attributes("-topmost", 1)
root.focus_force()

def download_csv(url, filename):
	http = PoolManager()
	response = str(http.request('GET', url).data)
	lines = str(response).strip("b'").replace("\\r", "").split("\\n")
	with open(filename, 'w') as file:
		for line in lines:
			file.write(line + "\n")

def generate_gif(graph_type, state, gif_file):
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

	df = pd.read_csv('../data/data.csv') # pandas dataframe with plot data
	with open('../data/data.csv', 'r') as file:
		num_lines = sum(1 for line in file)

	# decision tree to plot
	if graph_type == 1:
		for item in df['cases']: cases += (' ' + str(item))
		for item in df['deaths']: deaths += (' ' + str(item))
		os.system(f"gnuplot -e \"num_lines={num_lines}\" \
							-e \"cases = \'{cases}\'\" \
							-e \"deaths = \'{deaths}\'\" \
							-e \"gif_file = \'{gif_file}\'\" \
							-e \"state=\'{state.upper()}\'\" gnuplot_cumm.gp {the_void}")

	elif graph_type == 2 and state == "New York":
		for item in df['CASE_COUNT']: cases += (' ' + str(item))
		for item in df['DEATH_COUNT']: deaths += (' ' + str(item))
		for item in df['HOSPITALIZED_COUNT']: hosp += (' ' + str(item))
		os.system(f"gnuplot -e \"num_lines={num_lines}\" \
							-e \"cases = \'{cases}\'\" \
							-e \"deaths = \'{deaths}\'\" \
							-e \"hosp = \'{hosp}\'\" \
							-e \"gif_file = \'{gif_file}\'\" \
							-e \"state=\'{state.upper()}\'\" gnuplot_ny_noncumm.gp {the_void}")

	elif graph_type == 2:
		for item in df['cases']: cases += (' ' + str(int(item)))
		for item in df['deaths']: deaths += (' ' + str(int(item)))
		os.system(f"gnuplot -e \"num_lines={num_lines}\" \
							-e \"cases = \'{cases}\'\" \
							-e \"deaths = \'{deaths}\'\" \
							-e \"gif_file = \'{gif_file}\'\" \
							-e \"state=\'{state.upper()}\'\" gnuplot_noncumm.gp {the_void}")

def display_gif(gif_file):
	# if Operating System is Windows
	if os.name == 'nt':
		os.startfile(gif_file.replace("/","\\"))
	# otherwise this should work for Linux and MacOS
	else:
		os.system(f'xviewer {gif_file}')

# decorator function for displaying the program's runtime
def timer(original_func):
	def wrapper(*args, **kwargs):
		t1 = time.time()
		result = original_func(*args, **kwargs)
		t2 = time.time() - t1
		print(f'\n[Finished in {t2} sec]\n')
		return result
	return wrapper

@timer
def main(input_box=None):
    # declare variables
	abbrev = '' 		# user input: state abbreviation (i.e. 'NY')
	graph_type = ''		# user input: '1' for cummulative, '2' for noncummulative
	gif_file = ''		# filename for the output gif

	try:
		# get user input from dialog window
		try:
			state = input_box.result[0].title()
			if state == 'District Of Columbia': state = 'District of Columbia'
			graph_type = input_box.result[1]
			abbrev = state_to_abbrev[state]
		except TypeError:
			pass
		except KeyError:
			abbrev = input_box.result[0].upper()
			graph_type = input_box.result[1]
			state = abbrev_to_state[abbrev]

		# end program upon hitting 'Cancel' or [X]
		if abbrev == '' or (graph_type != 1 and graph_type != 2):
			root.destroy()
			raise SystemExit
		
		# decision tree to generate the GIF
		if abbrev != "US" and graph_type == 1:
			timestamp = date.today().strftime("%m_%d_%Y")
			file_list = glob.glob(f'../gifs/{abbrev.lower()}_cumm_*.gif')
			gif_file = f'../gifs/{abbrev.lower()}_cumm_{timestamp}.gif'
			
			try: os.remove('../data/data.csv')
			except FileNotFoundError: pass
			
			for file in file_list:
				try: os.remove(file)
				except FileNotFoundError: pass

			url = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'
			filename = '../data/raw_states_data.csv'
			download_csv(url, filename)
			df = pd.read_csv(filename)
			df.drop(df.index[df['state'] != abbrev_to_state[abbrev]], inplace=True)
			df.drop('state', axis=1, inplace=True)
			df.drop('fips', axis=1, inplace=True)
			df.to_csv('../data/data.csv', index=False)

			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(1, abbrev_to_state[abbrev], gif_file)

		elif abbrev == "US" and graph_type == 1:
			timestamp = date.today().strftime("%m_%d_%Y")
			file_list = glob.glob(f'../gifs/{abbrev.lower()}_cumm_*.gif')
			gif_file = f'../gifs/{abbrev.lower()}_cumm_{timestamp}.gif'
			
			try: os.remove('../data/data.csv')
			except FileNotFoundError: pass
			
			for file in file_list:
				try: os.remove(file)
				except FileNotFoundError: pass

			url = 'https://github.com/nytimes/covid-19-data/raw/master/us.csv'
			filename = '../data/raw_us_data.csv'
			download_csv(url, filename)
			shutil.copy2(filename, '../data/data.csv')

			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(1, abbrev_to_state[abbrev], gif_file)

		elif abbrev == "US" and graph_type == 2:
			timestamp = date.today().strftime("%m_%d_%Y")
			file_list = glob.glob(f'../gifs/{abbrev.lower()}_noncumm_*.gif')
			gif_file = f'../gifs/{abbrev.lower()}_noncumm_{timestamp}.gif'

			try: os.remove('../data/data.csv')
			except FileNotFoundError: pass
			
			for file in file_list:
				try: os.remove(file)
				except FileNotFoundError: pass

			url = 'https://github.com/nytimes/covid-19-data/raw/master/us.csv'
			filename = '../data/raw_us_data.csv'
			download_csv(url, filename)
			df_1 = pd.read_csv(filename)
			df_2 = df_1.loc[:,['cases', 'deaths']].diff() # cummulative --> noncummulative
			df_1.drop(['cases', 'deaths'], axis=1, inplace=True)
			df_merged = pd.concat([df_1, df_2], axis=1)
			df_merged.dropna(inplace=True)
			df_merged.astype({"cases":'int', "deaths":'int'})
			df_merged.to_csv('../data/data.csv', index=False)

			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(2, abbrev_to_state[abbrev], gif_file)

		elif abbrev == "NY" and graph_type == 2:
			timestamp = date.today().strftime("%m_%d_%Y")
			file_list = glob.glob(f'../gifs/{abbrev.lower()}_noncumm_*.gif')
			gif_file = f'../gifs/{abbrev.lower()}_noncumm_{timestamp}.gif'

			try: os.remove('../data/data.csv')
			except FileNotFoundError: pass
			
			for file in file_list:
				try: os.remove(file)
				except FileNotFoundError: pass

			url = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/archive/case-hosp-death.csv'
			filename = '../data/ny_curve.csv'
			download_csv(url, filename)
			shutil.copy2(filename, '../data/data.csv')

			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(2, abbrev_to_state[abbrev], gif_file)

		elif abbrev != "US" and graph_type == 2:
			timestamp = date.today().strftime("%m_%d_%Y")
			file_list = glob.glob(f'../gifs/{abbrev.lower()}_noncumm_*.gif')
			gif_file = f'../gifs/{abbrev.lower()}_noncumm_{timestamp}.gif'

			try: os.remove('../data/data.csv')
			except FileNotFoundError: pass
			
			for file in file_list:
				try: os.remove(file)
				except FileNotFoundError: pass
			
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'
			filename = '../data/raw_states_data.csv'
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
			df_merged.to_csv('../data/data.csv', index=False)

			with Spinner('\nYour graph will appear shortly...'):
				generate_gif(2, abbrev_to_state[abbrev], gif_file)

		display = messagebox.askyesno("Success!", "GIF Successfully Generated:\n\nShow GIF?")
		if display:	display_gif(gif_file)

		another_one = messagebox.askyesno("Info", "Would you like to track another state?")
		if another_one:
			top = Toplevel()
			center_window(top)
			top.update()
			top.withdraw()
			input_box = InputDialog(top)
			top.wm_attributes("-topmost", 1)
			top.focus_force()
			main(input_box)
			top.mainloop()

		exit()

	except Exception as e:
		messagebox.showerror(f"Failed: {repr(e)}", f"{traceback.format_exc()}")

if __name__ == '__main__':
	main(input_box)
	root.mainloop()