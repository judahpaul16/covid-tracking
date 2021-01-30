# ------------------ LOCAL MODULES --------------------
from state_dict import abbrev_to_state, state_to_abbrev
from dialog import MainDialog, InputDialog, CompareDialog, center
from spinner import Spinner
# ----------------- BULT-IN MODULES -------------------
from tkinter import Tk, messagebox
from itertools import repeat
import traceback
import shutil
import time
import glob
import os
# ----------------- EXTERNAL MODULES ------------------
import matplotlib.pyplot as plt
from urllib3 import PoolManager
from datetime import date
import pandas as pd
    
def restart():
    root.destroy()
    os.startfile("main.py")

def download_csv(url, filename):
	http = PoolManager()
	response = str(http.request('GET', url).data)
	lines = str(response).strip("b'").replace("\\r", "").split("\\n")
	with open(filename, 'w') as file:
		for line in lines:
			file.write(line + "\n")

def clear_data_files(files_to_remove):
	try: os.remove('../data/data.csv')
	except FileNotFoundError: pass
	
	for file in files_to_remove:
		try: os.remove(file)
		except FileNotFoundError: pass

def generate_chart(graph_type, output_file, state=None, style=None):
	# bind variables
	the_void = '' 	# a place for gnuplot warning messages to be sent
	num_lines = ''	# number of lines of plot data
	cases = ''		# plot data for graph legend
	deaths = '' 	# plot data for graph legend
	hosp = ''		# plot data for graph legend
	timestamp = date.today().strftime("%m/%d/%Y")

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
							-e \"output_file = \'{output_file}\'\" \
							-e \"state=\'{state.upper()}\'\" gnuplot_cumm_line.gp {the_void}")
		return

	elif graph_type == 2 and state == "New York":
		for item in df['CASE_COUNT']: cases += (' ' + str(item))
		for item in df['DEATH_COUNT']: deaths += (' ' + str(item))
		for item in df['HOSPITALIZED_COUNT']: hosp += (' ' + str(item))
		os.system(f"gnuplot -e \"num_lines={num_lines}\" \
							-e \"cases = \'{cases}\'\" \
							-e \"deaths = \'{deaths}\'\" \
							-e \"hosp = \'{hosp}\'\" \
							-e \"output_file = \'{output_file}\'\" \
							-e \"state=\'{state.upper()}\'\" gnuplot_ny_noncumm_line.gp {the_void}")
		return

	elif graph_type == 2:
		for item in df['cases']: cases += (' ' + str(int(item)))
		for item in df['deaths']: deaths += (' ' + str(int(item)))
		os.system(f"gnuplot -e \"num_lines={num_lines}\" \
							-e \"cases = \'{cases}\'\" \
							-e \"deaths = \'{deaths}\'\" \
							-e \"output_file = \'{output_file}\'\" \
							-e \"state=\'{state.upper()}\'\" gnuplot_noncumm_{style}.gp {the_void}")
		return

	elif graph_type == 3:
		os.system(f"gnuplot -e \"output_file = \'{output_file}\'\" gnuplot_bar.gp {the_void}")
		return

	elif graph_type == 4:
		# because gnuplot is a function plotter, it's easier to plot a pie chart with mathplotlib
		fig, (ax1,ax2) = plt.subplots(1,2,figsize=(14,6))
		fig.suptitle(f"State Share of COVID-19 Cases & Deaths As of {timestamp}\n" \
				"(Unadjusted for Population)", weight='bold')

		labels = df['state'].values.tolist()
		sizes = df['cases'].values.tolist()
		tmp = list(repeat(0.05, len(sizes)))
		tmp[sizes.index(max(sizes))] = 0.2 # only "explode" the largest slice
		explode = tuple(tmp)
		plt.text(x=0.49, y=0.52, s= "<- Cases", fontsize=12, ha="center",
				weight='bold', transform=fig.transFigure)
		ax1.pie(sizes, explode=explode, labels=labels, shadow=False,
				textprops={'size': 'smaller'}, rotatelabels=True, startangle=90)

		labels = df['state'].values.tolist()
		sizes = df['deaths'].values.tolist()
		tmp = list(repeat(0.05, len(sizes)))
		tmp[sizes.index(max(sizes))] = 0.2 # only "explode" the largest slice
		explode = tuple(tmp)
		plt.text(x=0.51, y=0.48, s= "Deaths ->", fontsize=12, ha="center",
				weight='bold', transform=fig.transFigure)
		ax2.pie(sizes, explode=explode, labels=labels, shadow=False,
				textprops={'size': 'smaller'}, rotatelabels=True, startangle=90)

		plt.tight_layout()
		plt.axis('equal')  # ensures the pie is drawn as a circle
		plt.savefig(output_file)
		return
	
	elif graph_type == 5:
		x = df['cases']
		y = df['deaths']

		annotations = list()
		for entry in range(len(df['state'])):
			annotations.append(state_to_abbrev[df['state'].values[entry]])

		xy_ratio = list()
		for i in range(len(x)):
			xy_ratio.append((y.values[i] / x.values[i]))

		plt.figure(figsize=(12,6))
		plt.title("COVID-19 Fifty State Comparison: Cases vs. Deaths")
	
		for i, label in enumerate(annotations):
			plt.annotate(label, (x[i], y[i]))

		plt.xlabel('Cases (millions)')
		plt.ylabel('Deaths')
		plt.scatter(x, y, c=xy_ratio, alpha=0.5)
		cbar = plt.colorbar()
		cbar.set_label('Case Fatality Rate')
		plt.style.use('seaborn')
		plt.tight_layout()
		plt.savefig(output_file)

def display_output(output_file):
	# if Operating System is Windows
	if os.name == 'nt':
		os.startfile(output_file.replace("/","\\"))
	# otherwise this should work for Linux and MacOS
	else:
		os.system(f'xviewer {output_file}')

def another_one(dialog_1=None, dialog_2=None):
	another_one = messagebox.askyesno("Info", "Would you like to generate more charts?")
	if another_one:
		restart()
	return

# decorator function for displaying the program's runtime
def timer(original_func):
	def wrapper(*args, **kwargs):
		t1 = time.time()
		result = original_func(*args, **kwargs)
		t2 = time.time() - t1
		print(f'\n[Finished in {t2} sec]')
		another_one()
		exit()
	return wrapper

@timer
def main(dialog_2=None):
    # declare variables
	abbrev = '' 			# user input: state abbreviation (i.e. 'NY')
	graph_type = ''			# user input: '1' for cummulative, '2' for noncummulative, '3' for bar graph
	output_file = ''		# filename for the output
	entry_list = []			# for comparing multiple states
	style = ''
	abbrevs = []			# list of abbreviations from entry list
	CURR_DIR = os.getcwd() 	# current working directory

	if CURR_DIR[-3:] != 'src': os.chdir(CURR_DIR + "/src")

	try:
		# end program upon hitting 'Cancel' or [X] on dialog window
		if not dialog_2.validated:
			root.destroy()
			raise SystemExit
		
		# get user input from dialog window
		if dialog_2.graph_type in [1, 2]:
			try:
				state = dialog_2.state.title()
				if state == 'District Of Columbia': state = 'District of Columbia'
				graph_type = dialog_2.graph_type
				abbrev = state_to_abbrev[state]
			except KeyError:
				abbrev = dialog_2.state.upper()
				graph_type = dialog_2.graph_type
				state = abbrev_to_state[abbrev]
		elif dialog_2.graph_type in [3, 4, 5]:
			graph_type = dialog_2.graph_type
			entry_list = dialog_2.entry_list_values
			
		# decision tree to generate the output file
		if abbrev != "US" and graph_type == 1: # cummulative state data over time
			timestamp = date.today().strftime("%m_%d_%Y")
			files_to_remove = glob.glob(f'../gifs/{abbrev.lower()}_cumm_line_*.gif')
			output_file = f'../gifs/{abbrev.lower()}_cumm_line_{timestamp}.gif'
			
			clear_data_files(files_to_remove)

			# get new data
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'
			data_file = '../data/raw_states_data.csv'
			download_csv(url, data_file)
			df = pd.read_csv(data_file)
			df.drop(df.index[df['state'] != abbrev_to_state[abbrev]], inplace=True)
			df.drop('state', axis=1, inplace=True)
			df.drop('fips', axis=1, inplace=True)
			df.to_csv('../data/data.csv', index=False)

			with Spinner('\nYour graph will appear shortly...'):
				generate_chart(1, output_file, abbrev_to_state[abbrev])

		elif abbrev == "US" and graph_type == 1: # cummulative US data over time
			timestamp = date.today().strftime("%m_%d_%Y")
			files_to_remove = glob.glob(f'../gifs/{abbrev.lower()}_cumm_line_*.gif')
			output_file = f'../gifs/{abbrev.lower()}_cumm_line_{timestamp}.gif'
			
			clear_data_files(files_to_remove)

			# get new data
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us.csv'
			data_file = '../data/raw_us_data.csv'
			download_csv(url, data_file)
			shutil.copy2(data_file, '../data/data.csv')

			with Spinner('\nYour graph will appear shortly...'):
				generate_chart(1, output_file, abbrev_to_state[abbrev])

		elif abbrev == "US" and graph_type == 2: # non-cummulative US data over time
			histogram = messagebox.askyesno("Info", \
				"Would you like to display the chart as a \'histogram\'?\n\n[Default: \'line\']")
			if histogram: style = "histogram"
			else: style = "line"

			timestamp = date.today().strftime("%m_%d_%Y")
			files_to_remove = glob.glob(f'../gifs/{abbrev.lower()}_noncumm_{style}_*.gif')
			output_file = f'../gifs/{abbrev.lower()}_noncumm_{style}_{timestamp}.gif'

			clear_data_files(files_to_remove)

			# get new data
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us.csv'
			data_file = '../data/raw_us_data.csv'
			download_csv(url, data_file)
			df_1 = pd.read_csv(data_file)
			df_2 = df_1.loc[:,['cases', 'deaths']].diff() # cummulative --> noncummulative
			df_1.drop(['cases', 'deaths'], axis=1, inplace=True)
			df_merged = pd.concat([df_1, df_2], axis=1)
			df_merged.dropna(inplace=True)
			df_merged.astype({"cases":'int', "deaths":'int'})
			df_merged.to_csv('../data/data.csv', index=False)

			with Spinner('\nYour graph will appear shortly...'):
				generate_chart(2, output_file, abbrev_to_state[abbrev], style)

		elif abbrev == "NY" and graph_type == 2: # non-cummulative New York data over time
			timestamp = date.today().strftime("%m_%d_%Y")
			files_to_remove = glob.glob(f'../gifs/{abbrev.lower()}_noncumm_{style}_*.gif')
			output_file = f'../gifs/{abbrev.lower()}_noncumm_{timestamp}.gif'

			clear_data_files(files_to_remove)

			# get new data
			url = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/archive/case-hosp-death.csv'
			data_file = '../data/ny_curve.csv'
			download_csv(url, data_file)
			shutil.copy2(data_file, '../data/data.csv')

			with Spinner('\nYour graph will appear shortly...'):
				generate_chart(2, output_file, abbrev_to_state[abbrev])

		elif abbrev != "US" and graph_type == 2: # non-cummulative state data over time
			histogram = messagebox.askyesno("Info", \
				"Would you like to display the chart as a \'histogram\'?\n\n[Default: \'line\']")
			if histogram: style = "histogram"
			else: style = "line"

			timestamp = date.today().strftime("%m_%d_%Y")
			files_to_remove = glob.glob(f'../gifs/{abbrev.lower()}_noncumm_{style}_*.gif')
			output_file = f'../gifs/{abbrev.lower()}_noncumm_{style}_{timestamp}.gif'

			clear_data_files(files_to_remove)
			
			# get new data
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'
			data_file = '../data/raw_states_data.csv'
			download_csv(url, data_file)
			df_1 = pd.read_csv(data_file)
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
				generate_chart(2, output_file, abbrev_to_state[abbrev], style)

		elif graph_type == 3: # state comparison: bar chart
			timestamp = date.today().strftime("%m_%d_%Y")
			for entry in entry_list:
				abbrevs.append(state_to_abbrev[entry].lower())
			abbrevs_string = str(abbrevs).replace('\', \'','_').strip('[,\']')
			files_to_remove = glob.glob(f"../images/{abbrevs_string}_compare_bar_*.png")
			output_file = f"../images/{abbrevs_string}_compare_bar_{timestamp}.png"

			clear_data_files(files_to_remove)

			# get new data
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'
			data_file = '../data/raw_states_data.csv'
			download_csv(url, data_file)
			df_1 = pd.read_csv(data_file)
			df_1.drop('date', axis=1, inplace=True)
			df_1.drop('fips', axis=1, inplace=True)
			df_1.dropna(inplace=True)
			df_2 = None

			for entry in entry_list:
				df_2 = pd.concat([df_2, df_1.drop(df_1.index[df_1['state'] != entry]).tail(1)], axis=0)

			df_2.dropna(inplace=True)
			df_2.drop_duplicates(keep = 'first', inplace = True) 
			df_2.astype({"cases":'int', "deaths":'int'})
			df_2.to_csv('../data/data.csv', index=False)

			with Spinner('\nYour graph will appear shortly...'):
				generate_chart(3, output_file)

		elif graph_type == 4: # state comparison: pie chart
			timestamp = date.today().strftime("%m_%d_%Y")
			files_to_remove = glob.glob(f"../images/us_compare_pie_*.png")
			output_file = f"../images/us_compare_pie_{timestamp}.png"

			clear_data_files(files_to_remove)

			# get new data
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'
			data_file = '../data/raw_states_data.csv'
			download_csv(url, data_file)
			df_1 = pd.read_csv(data_file)
			df_1.drop('date', axis=1, inplace=True)
			df_1.drop('fips', axis=1, inplace=True)
			df_1.dropna(inplace=True)
			df_2 = None

			for item in state_to_abbrev:
				df_2 = pd.concat([df_2, df_1.drop(df_1.index[df_1['state'] != item]).tail(1)], axis=0)

			df_2.dropna(inplace=True)
			df_2.drop_duplicates(keep = 'first', inplace = True) 
			df_2.astype({"cases":'int', "deaths":'int'})
			df_2.to_csv('../data/data.csv', index=False)
			
			with Spinner('\nYour graph will appear shortly...'):
				generate_chart(4, output_file)

		elif graph_type == 5: # state comparison: scatter plot cases vs deaths
			timestamp = date.today().strftime("%m_%d_%Y")
			files_to_remove = glob.glob(f"../images/us_cases_deaths_scatter_*.png")
			output_file = f"../images/us_cases_deaths_scatter_{timestamp}.png"

			clear_data_files(files_to_remove)
			url = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'
			data_file = '../data/raw_states_data.csv'
			download_csv(url, data_file)
			df_1 = pd.read_csv(data_file)
			df_1.drop('date', axis=1, inplace=True)
			df_1.drop('fips', axis=1, inplace=True)
			df_1.dropna(inplace=True)
			df_2 = None

			for item in state_to_abbrev:
				df_2 = pd.concat([df_2, df_1.drop(df_1.index[df_1['state'] != item]).tail(1)], axis=0)

			df_2.dropna(inplace=True)
			df_2.drop_duplicates(keep = 'first', inplace = True) 
			df_2.astype({"cases":'int', "deaths":'int'})
			df_2.to_csv('../data/data.csv', index=False)

			with Spinner('\nYour graph will appear shortly...'):
				generate_chart(5, output_file)

		display = messagebox.askyesno("Success!", "Chart Successfully Generated:\n\nShow Chart?")
		if display:	display_output(output_file)

	except Exception as e:
		messagebox.showerror(f"Failed: {repr(e)}", f"{traceback.format_exc()}")
		root.destroy()
		raise SystemExit

if __name__ == '__main__':
	# popup tkinter gui for user input
	root = Tk()
	root.update()
	center(root)
	root.withdraw()

	dialog_1 = MainDialog(root)
	dialog_2 = None

	# end program upon hitting 'Cancel' or [X] on dialog window
	if not dialog_1.validated:
		root.destroy()
		raise SystemExit

	if dialog_1.compare: dialog_2 = CompareDialog(root)
	else: dialog_2 = InputDialog(root)

	root.wm_attributes("-topmost", 1)
	root.focus_force()
	main(dialog_2)
	root.mainloop()