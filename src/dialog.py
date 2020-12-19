# ------------------ LOCAL MODULES --------------------
from state_dict import abbrev_to_state, state_to_abbrev
# ----------------- BUILT-IN MODULES ------------------
from tkinter import Label, Entry, Checkbutton, StringVar, IntVar
from tkinter.simpledialog import Dialog
from tkinter.ttk import Combobox
import time

class InputDialog(Dialog):
	# Inherits tkinter.simpledialog's Dialog Class
    # organize the layout of the input box here
    def body(self, master):
        self.geometry("360x180")
        self.winfo_toplevel().title("COVID Tracking With GNUPlot")
        states = []
        for item in state_to_abbrev: states.append(item)

        Label(master, text="Select the State and Graph\nType For Visualization",
            font=('Roboto', 12, 'bold')).grid(row=0, column=0, columnspan=2, rowspan=2)
        Label(master, text="State   - - - - -> \n\nGraph Type  - - - ->",
            font=('Roboto', 10)).grid(row=2, rowspan=3)
        
        self.e1 = Combobox(master, textvariable=StringVar(), values=states)
        self.e1.grid(row=2, column=1, sticky='we')

        check_1 = IntVar()
        check_2 = IntVar()
        
        def checkcheckbox():
            if check_1.get() and check_2.get():
                warning.config(text="Select one graph type.", fg="red")
                check_btn1.deselect()
                check_btn2.deselect()
                self.e2 = 0
            elif check_1.get() and not check_2.get():
                warning.config(text="")
                self.e2 = 1
            elif check_2.get() and not check_1.get():
                warning.config(text="")
                self.e2 = 2
        
        warning = Label(master, text="", font=('roboto', 10))
        warning.grid(row=5, column=0, columnspan=2)
        check_btn1 = Checkbutton(master, text = 'Cumm.', variable = check_1,
            onvalue = 1, offvalue = 0, command=checkcheckbox)
        check_btn2 = Checkbutton(master, text = 'N-Cumm.', variable = check_2,
            onvalue = 1, offvalue = 0, command=checkcheckbox)
        check_btn1.grid(row=4, column=1, sticky='w')
        check_btn2.grid(row=4, column=1, sticky='e')

        return self.e1 # initial focus
        
    # executes upon hitting 'Okay'
    def validate(self):
        try:
            state = str(self.e1.get())
            graph_type = int(self.e2)
            self.result = state, graph_type
        except AttributeError:
            pass

        if state == '' or (graph_type != 1 and graph_type != 2):
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
