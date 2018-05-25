# This class is used for the destroy interface. This class moves the inputted hard drives into the hard drive destruction project
# and marks them all as completed with the selected time and method

import tkinter as tk
import tkinter.ttk as ttk
import datetime
import time
import sys
import google_sheet_logging as gslog
import error_check as ec
import asana_hook as ashook
import drive_hook as dhook
import os
from tkinter import *
import tkinter.font as tkFont

import graphic_interface as g
import cert_check_interface as cc


def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
   base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

# The main window (sans popups) is an extension of a TK frame
# This class houses all of the GUI widgets
class Application(tk.Frame):

    # Initilizes scroll bar, auto resizing
    # Calls populate function to create vendor entry widgets
    def __init__(self, master=None):

        self.master = master

        super().__init__(master)
        
        self.canvas = tk.Canvas(master, borderwidth=50, background="#004F2E")
        self.mainframe = tk.Frame(self.canvas, background="#fff")
        self.vsb = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.mainframe, anchor="ne", 
                                    tags="self.mainframe")

        self.mainframe.bind("<Configure>", self.onFrameConfigure)

        self.populate(self.mainframe)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def make_separator_at_row(self, r):
        ttk.Separator(self.mainframe ,orient=tk.HORIZONTAL).grid(row=r, column=0, columnspan=14, sticky='ew', pady=20)

    # HDD Info Frame Rows 3+
    def ask_for_number_of_HDDS(self, f):
        self.num_hdd_label = tk.Label(f, text="Count total number of drives: ")
        self.num_hdd_entry = tk.Entry(f, width=0)
        self.num_hdd_label.grid(row=2, column=0)
        self.num_hdd_entry.grid(row=2, column=1, columnspan=9, sticky='ew')

        self.num_hdd_enter_btn = tk.Button(f, text="Start", width=0)
        self.num_hdd_enter_btn["command"] = lambda: self.generate_input(self.num_hdd_entry.get(), f)
        self.num_hdd_enter_btn.grid(row=3, column=1, columnspan=8, sticky='ew', pady=20)


    def onMouseWheel(self, event):
        if (self.mainframe.winfo_height() <= self.master.winfo_height()):
            self.mainframe.unbind_all("<MouseWheel>")
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def generate_input(self, HDD, f):
        # Saves number of HDDS in global variable
        if ec.check_for_null_field(HDD, self.num_hdd_entry):
            self.p = WarningPopup("You left the number of HDDs blank!")
            return
        self.NUM_HDDS = int(HDD)
        # Removes the entry widgets for GUI
        self.num_hdd_label.grid_forget()
        self.num_hdd_entry.grid_forget()
        self.num_hdd_enter_btn.grid_forget()
        # Generates barcode input widgets
        self.barcode_input(self.NUM_HDDS, f)
        self.status_input(self.NUM_HDDS, f)
        self.make_separator_at_row((self.NUM_HDDS+7))
        self.run_button(self.NUM_HDDS, f)
        self.mainframe.bind_all("<MouseWheel>", self.onMouseWheel)

    def populate(self, mainframe):

        self.technician_input(mainframe)
        self.make_separator_at_row(5)
        self.ask_for_number_of_HDDS(mainframe)
        self.back_button(mainframe)
        self.start_time = time.time()

    def barcode_input(self, num_hdds, f):
        self.barcodes_container = []

        for i in range(num_hdds):
            self.l = tk.Label(f, text="Serial Number: ")
            self.e = tk.Entry(f, width=30)
            self.l.grid(row=i+6, column=0)
            self.e.grid(row=i+6, column=1, columnspan=6, sticky='ew')
            self.barcodes_container.append([self.e, 0])

    def technician_input(self, f):

        self.technician_input_label = tk.Label(f, text="Technician: ")
        # Add a grid

        options = {
        'Preston Wong',
        'Patrick Carroll',
        'Omar Guzman',
        'James Jack',
        'Hayk Tahmasian',
        'Oscar Manzo',
        'AJ',
        'Hanli Su'
        }

        self.variable = StringVar()
        self.variable.set("Preston Wong")
        self.menu = OptionMenu(f, self.variable, *options, command = self.func)
        
        self.menu.grid(row = 0, column = 12)

        self.technician_input_label.grid(row=0, column=8, columnspan=3, padx=(150, 5), pady=5)
        self.func(self.variable)
        # self.technician_input_entry.grid(row=0, column=11, columnspan=3, padx=5, pady=5)  

    def func(self, value):
        self.technician_input_entry = self.variable.get()
        self.technician = self.technician_input_entry
        print("tech entry", self.technician_input_entry)


    def run_button(self, HDD, f):
        self.run_button = tk.Button(f, text="Run")
        self.run_button["command"] = lambda: self.run_logic()
        self.run_button.grid(row=HDD+12, column=2, columnspan=10, pady=(20, 20), sticky='ew')

    def push_asana(self, top):
        self.start_status(self.NUM_HDDS)
        ashook.destroy(self.automatic_inventory, top, self.priority, self, self.technician)
    
    def start_status(self, total):
        self.red_rectangle = self.status_bar_background.create_rectangle(100, 0, 600, 30, fill="red")
        self.green_rectangle = self.status_bar_background.create_rectangle(0, 0, 0, 0, fill="green")
        self.status_bar_label["text"] = "Pushing to Asana: 0/{}".format(total)
        self.update()


    def update_status(self, done):
        self.percent = int((done / self.NUM_HDDS) * 500)
        self.status_bar_background.coords(self.red_rectangle, 100+self.percent, 0, 600, 30)
        self.status_bar_background.coords(self.green_rectangle, 100, 0, 100+self.percent, 30)
        self.status_bar_label["text"] = "Pushing to Asana: {}/{}".format(done, self.NUM_HDDS)
        self.update()

    def finish_status(self):
        self.status_bar_background.coords(self.red_rectangle, 100, 0, 600, 30)
        self.status_bar_background.coords(self.green_rectangle, 100, 0, 600, 30)
        self.status_bar_label["text"] = "Updating Google Sheets..."
        self.update()

    def back_button(self,f):
        self.back_button = tk.Radiobutton(f, text="Back", indicatoron=0, value="Back", padx = 50, command = lambda : self.main_menu(f))
        self.back_button.grid(row=0, column=0)

    def main_menu(self, master):
        # print("Hi")
        self.master.destroy()
        root = tk.Tk()
        root.iconbitmap(resource_path('img/icon.ico'))
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("{}x{}+0+0".format(500, 380))
        root.wm_title("Cerebot")
        mainframe = tk.Frame(master=root, background = "#9BE7FF")
        mainframe.pack(side="top", fill="both", expand=True)

        helv36 = tkFont.Font(family='Helvetica', size=36, weight='bold')
        
        inv = tk.Button(mainframe, text="Inventory", padx='10', pady='10', font = helv36, borderwidth='5' , background = "#FF4435")
        inv["command"] = lambda: self.start_this_programs(True, False, root)
        inv.pack(side="top")

        cert = tk.Button(mainframe, text="Certification Check", padx='10', pady='10', font = helv36, borderwidth='5', background = "#005EC4")
        cert["command"] = lambda: self.start_this_programs(False, True, root)
        cert.pack(side='top')

        destroy = tk.Button(mainframe, text="Destruction", padx='10', pady='10', font = helv36, borderwidth='5', background = "#004F2E")
        destroy["command"] = lambda: self.start_this_programs(False, False, root)
        destroy.pack(side='top')

    def start_this_programs(self, true_if_inv, true_if_cert, parent):
        if true_if_inv:
            g.run_gui(parent)
        elif true_if_cert:
            cc.run_gui(parent)
        else:
            run_gui(parent)  

    def run_logic(self):
        # technician check
        # if not ec.STOP_PARSING:
        #     self.technician = ec.validate_technician(self.technician_input_entry.get(), self.technician_input_entry)
        #     if self.technician == "None":
        #         self.p = WarningPopup("Technician not found. Please check your spelling")
        #         self.wait_window(self.p)
        # Second count of hard-drives
        # if not ec.STOP_PARSING:
        #     self.validationPopup = ValidationPopup("Recount the number of hard-drives to confirm", self.NUM_HDDS)
        #     self.wait_window(self.validationPopup)
        if not ec.STOP_PARSING:
            # Barcode check in error_check module
            for item in self.barcodes_container:
                item[1] = item[0].get()
            ec.parse_barcodes(self.barcodes_container, self)

        if ec.STOP_PARSING:
            ec.STOP_PARSING = False

        #Asana Pushing and Checking
        for index, item in enumerate(self.barcodes_container):
            self.status_container[index][0]["bg"]="yellow"
            self.status_container[index][0]["text"]="Processing..."
            self.update()
            result = ashook.destroy(item[1], self.technician, True)
            if result == "ERROR":
                self.status_container[index][0]["bg"]="firebrick1"
                self.status_container[index][0]["text"]="NOT FOUND"

                deletingPeriodSerialNumber = item[1].replace('.', '', 1)
                self.doublecheck = ashook.destroy(deletingPeriodSerialNumber, self.technician, True)
                if self.doublecheck == "ERROR":
                    self.status_container[index][0]["bg"]="firebrick1"
                    self.status_container[index][0]["text"]="NOT FOUND"
                    # print("Before adding period item1", item[1])
                    addingPeriod = item[1] + "."
                    # print("Adding Period: ", addingPeriod)
                    self.doublecheck = ashook.destroy(addingPeriod, self.technician, True)
                    # print("After add period: ", self.doublecheck)
                    if self.doublecheck == "ERROR":
                        # self.num_missed_drives += 1
                        self.status_container[index][0]["bg"]="firebrick1"
                        self.status_container[index][0]["text"]="NOT FOUND"

                else:
                    # self.num_checked_drives += 1
                    self.status_container[index][0]["bg"]="SeaGreen1"
                    self.status_container[index][0]["text"]="Success"
            else:
                self.status_container[index][0]["bg"]="SeaGreen1"
                self.status_container[index][0]["text"]="SUCCESS"



    def status_input(self, num_hdds, f):
        self.status_container = []

        for i in range(num_hdds):
            self.status_button = tk.Button(f, text="Pending")
            self.status_button["bg"]="peach puff"
            self.status_button.grid(row=i+6, column=8, columnspan=4, sticky='ew')
            self.status_container.append([self.status_button, 0])

    def dummy(self, top):
        print("Dummy function")
        top.destroy()

    def api_hooks(self, top):
        top.destroy()

        #self.p = PromptPopup("Asana", "Asana hook please wait...")
        time.sleep(1)
        self.push_asana(self.p)
        time.sleep(1)
        #self.wait_window(self.p)
        time.sleep(1)
        #self.p = PromptPopup("Logging", "Logging hooks please wait...")
        time.sleep(1)
        self.make_log(self.p) # Logging function right below
        time.sleep(1)
        #self.wait_window(self.p)
        self.status_bar_label["text"] = "Inventoried: {} \nHDDS\n\nEwasted: {} \nHDDS\n\n".format(self.num_inventoried_drives, self.num_ewasted_drives)
        self.run_button.grid_forget()
        self.clear_errors_button.grid_forget()
        self.p = PromptPopup("Done",
            "Inventoried: {} \nHDDS\n\nEwasted: {} \nHDDS\n\n".format(self.num_inventoried_drives,
                                                                                    self.num_ewasted_drives
                                                                                    ),
            [["Exit", lambda: self.kill_program(self.p)]])
        self.wait_window(self.p)
        self.quit()
        
class WarningPopup(tk.Toplevel):
    def __init__(self, message):
        super().__init__()
        self.attributes("-topmost", True)
        self.focus_force()
        self.grab_set()
        self.title="WARNING"
        self.msg = tk.Message(self, text=message)
        self.msg.pack()
        self.button = tk.Button(self, text="Dismiss", command=self.destroy)
        self.button.pack()

class ValidationPopup(tk.Toplevel):
    def __init__(self, message, NUM_HDDS):
        super().__init__()
        self.attributes("-topmost", True)
        self.focus_force()
        self.grab_set()
        self.title="Entry Needed"
        self.msg = tk.Message(self, text=message)
        self.msg.pack()
        self.entry = tk.Entry(self)
        self.entry.pack()
        self.button = tk.Button(self, text="Dismiss", command=lambda: ec.validate_num_hdds(self, self.entry, NUM_HDDS))
        self.button.pack()

    

# Called from asana_automate.py
# Constructor that creates the main window object
def run_gui(parent):
    print(resource_path('img/icon.ico'))
    parent.destroy()
    root = tk.Tk()
    root.iconbitmap(resource_path('img/icon.ico'))
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    #root.geometry("{}x{}+0+0".format(w, h))
    root.geometry("{}x{}+0+0".format(750, h-500))
    root.wm_title("Destruction -- Cerebot")
    app = Application(master=root)
    app.pack(side="top", fill="both", expand=True)
    app.mainloop()

class PromptPopup(tk.Toplevel):
    def __init__(self, title, message, args=None):
        super().__init__()
        self.attributes("-topmost", True)
        self.focus_force()
        self.grab_set()
        self.title(title)
        self.msg = tk.Message(self, text=message)
        self.msg.pack()
        if args:
            for btn in args:
                self.button = tk.Button(self, text=btn[0], command=btn[1])
                self.button.pack()