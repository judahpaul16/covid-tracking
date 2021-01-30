# ------------------ LOCAL MODULES --------------------
from logging import warning
from os import replace
from state_dict import abbrev_to_state, state_to_abbrev
# ----------------- BUILT-IN MODULES ------------------
from tkinter import Label, Entry, Checkbutton, StringVar, IntVar
from tkinter.simpledialog import Dialog
from tkinter.ttk import Combobox
import time

class MainDialog(Dialog):
    # Inherits tkinter.simpledialog's Dialog Class
    compare = None
    validated = False

    def body(self, master):
        check_1 = IntVar()
        check_2 = IntVar()
        self.geometry("350x150")
        self.winfo_toplevel().title("COVID Tracking")

        Label(master, text="Compare States or\nTrack Individual States?",
            font=('Roboto', 12, 'bold')).grid(row=0, column=0, columnspan=2, rowspan=2)
        
        def checkcheckbox():
            if check_1.get() and check_2.get():
                self.warning.config(text="Select only one option", fg="red")
                check_btn1.deselect()
                check_btn2.deselect()
                self.e1 = 0
            elif check_1.get() and not check_2.get():
                self.warning.config(text="")
                self.e1 = 1
            elif check_2.get() and not check_1.get():
                self.warning.config(text="")
                self.e1 = 2

        self.warning = Label(master, text="", font=('roboto', 10))
        self.warning.grid(row=3, column=0, columnspan=2)
        check_btn1 = Checkbutton(master, text = 'Compare States', variable = check_1,
            onvalue = 1, offvalue = 0, command=checkcheckbox)
        check_btn2 = Checkbutton(master, text = 'Track Single State', variable = check_2,
            onvalue = 1, offvalue = 0, command=checkcheckbox)
        check_btn1.grid(row=2, column=0, columnspan=2, sticky='we')
        check_btn2.grid(row=3, column=0, columnspan=2, sticky='we')

    def validate(self): # executes upon hitting 'Okay'
        if int(self.e1) == 1:
            self.compare = True
            self.validated = True
            return 1
        elif int(self.e1) == 2:
            self.compare = False
            self.validated = True
            return 1
        elif not self.compare:
            return 0

class InputDialog(Dialog):
	# Inherits tkinter.simpledialog's Dialog Class
    states = []
    state = None
    graph_type = None
    warning = None
    validated = False

    def body(self, master):
        check_1 = IntVar()
        check_2 = IntVar()
        self.geometry("360x180")
        self.winfo_toplevel().title("COVID Tracking")

        for item in state_to_abbrev: self.states.append(item)

        Label(master, text="Select the State and Graph\nType For Visualization",
            font=('Roboto', 12, 'bold')).grid(row=0, column=0, columnspan=2, rowspan=2)
        Label(master, text="State   - - - - -> \n\nGraph Type  - - - ->",
            font=('Roboto', 10)).grid(row=2, rowspan=3)
        
        self.e1 = Combobox(master, textvariable=StringVar(), values=self.states)
        self.e1.grid(row=2, column=1, sticky='we')

        def checkcheckbox():
            if check_1.get() and check_2.get():
                self.warning.config(text="Select one graph type.", fg="red")
                check_btn1.deselect()
                check_btn2.deselect()
                self.e2 = 0
            elif check_1.get() and not check_2.get():
                self.warning.config(text="")
                self.e2 = 1
            elif check_2.get() and not check_1.get():
                self.warning.config(text="")
                self.e2 = 2
        
        self.warning = Label(master, text="", font=('roboto', 10))
        self.warning.grid(row=5, column=0, columnspan=2)
        check_btn1 = Checkbutton(master, text = 'Cumm.', variable = check_1,
            onvalue = 1, offvalue = 0, command=checkcheckbox)
        check_btn2 = Checkbutton(master, text = 'N-Cumm.', variable = check_2,
            onvalue = 1, offvalue = 0, command=checkcheckbox)
        check_btn1.grid(row=4, column=1, sticky='w')
        check_btn2.grid(row=4, column=1, sticky='e')

        return self.e1 # initial focus
        
    def validate(self): # executes upon hitting 'Okay'
        try:
            self.state = str(self.e1.get())
            self.graph_type = int(self.e2)
        except AttributeError:  
            pass

        if self.state == '' or self.graph_type not in [1, 2]:
            return 0
        else:
            self.validated = True
            return 1

class CompareDialog(Dialog):
    # Inherits tkinter.simpledialog's Dialog Class
    states = []
    entry_list = []
    entry_list_values = []
    graph_type = None
    warning = None
    validated = False

    def body(self, master):
        check_1 = IntVar()
        check_2 = IntVar()
        check_3 = IntVar()
        self.geometry("300x385")
        self.winfo_toplevel().title("COVID Tracking")

        for item in state_to_abbrev: self.states.append(item)

        Label(master, text="Select or Enter up to\n10 States to Compare",
            font=('Roboto', 12, 'bold')).grid(row=0, column=0, columnspan=2, rowspan=2)

        self.warning = Label(master, text="", font=('roboto', 10))
        self.warning.grid(row=2, column=0, columnspan=2)
        self.warning.config(text="")

        for n in range(10):
            entry = Combobox(master, textvariable=StringVar(), values=self.states)
            entry.grid(row=n+8, column=0, columnspan=2, sticky='we')
            self.entry_list.append(entry)

        def checkcheckbox():
            if (check_1.get() and check_2.get()) or \
                (check_2.get() and check_3.get()) or \
                (check_1.get() and check_3.get()):

                self.warning.config(text="Select one graph type.", fg="red")
                check_btn1.deselect()
                check_btn2.deselect()
                check_btn3.deselect()
            elif check_1.get() and not check_2.get() and not check_3.get():
                self.warning.config(text="")
                self.graph_type = 3
            elif check_2.get() and not check_1.get() and not check_3.get():
                self.warning.config(text="")
                self.graph_type = 4
            elif check_3.get() and not check_1.get() and not check_2.get():
                self.warning.config(text="")
                self.graph_type = 5
            
        check_btn1 = Checkbutton(master, text = 'Bar Chart', variable = check_1,
            onvalue = 1, offvalue = 0, command=checkcheckbox)
        check_btn2 = Checkbutton(master, text = 'Pie Chart', variable = check_2,
            onvalue = 1, offvalue = 0, command=checkcheckbox)
        check_btn3 = Checkbutton(master, text = 'Scatter Chart', variable = check_3,
            onvalue = 1, offvalue = 0, command=checkcheckbox)
        check_btn1.grid(row=4, column=0, columnspan=2, sticky='we')
        check_btn2.grid(row=3, column=0, sticky='we')
        check_btn3.grid(row=3, column=1, sticky='we')

        return self.entry_list[0] # initial focus
    
    def checkDuplicates(self):
        seen = set()
        for entry in self.entry_list:
            if str(entry.get()) in seen and str(entry.get()) != "":
                return True
            seen.add( str(entry.get()))
        return False

    def validate(self): # executes upon hitting 'Okay'
        if self.checkDuplicates():
            self.warning.config(text="You cannot compare a state with itself.", fg="red")
            return 0

        for entry in self.entry_list:
            self.entry_list_values.append(str(entry.get()))
        while ("" in self.entry_list_values) :
            self.entry_list_values.remove("")

        if len(self.entry_list_values) > 1 and self.graph_type == 3:
            self.validated = True
            return 1
        elif len(self.entry_list_values) == 0 and self.graph_type in [4, 5]:
            self.validated = True
            return 1

        self.warning.config(text="This option compares all states.\nClear all entries to continue.", fg="red")
        self.states.clear()
        self.entry_list_values.clear()
        return 0

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