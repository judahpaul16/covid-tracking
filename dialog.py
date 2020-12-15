from tkinter import Label, Entry, StringVar
from tkinter import simpledialog as tk_input

class MainDialog(tk_input.Dialog):
	# Inherits tkinter.simpledialog's Dialog Class
    # organize the layout of the input box here
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

    # executes upon hitting 'Okay'
    def validate(self):
        abbrev = str(self.e1.get())
        graph_type = int(self.e2.get())
        self.result = abbrev, graph_type
        if abbrev == '' or (graph_type != 1 and graph_type != 2):
            return 0
        else:
            return 1

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