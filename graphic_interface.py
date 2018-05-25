import tkinter as tk
import tkinter.ttk as ttk
import datetime
import time
import sys
import google_sheet_logging as gslog
import error_check as ec
import asana_hook as ashook
import tkinter.font as tkFont
# from asana_automate import main

import os
from tkinter import *
import cert_check_interface as cc
import destroy_interface as di

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
		self.canvas = tk.Canvas(master, borderwidth=0, background="#FF4435")
		self.mainframe = tk.Frame(self.canvas, background="#ffffff")
		self.vsb = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.vsb.set)

		self.vsb.pack(side="right", fill="y")
		self.canvas.pack(side="left", fill="both", expand=True)
		self.canvas.create_window((4,4), window=self.mainframe, anchor="ne", 
									tags="self.mainframe")

		self.mainframe.bind("<Configure>", self.onFrameConfigure)

		self.populate(self.mainframe)
	
	def onMouseWheel(self, event):
		if (self.mainframe.winfo_height() <= self.master.winfo_height()):
			self.mainframe.unbind_all("<MouseWheel>")
		self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

	def onFrameConfigure(self, event):
		'''Reset the scroll region to encompass the inner frame'''
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	# Vendor Info Frame, with entry to input number of HDDS
	def populate(self, mainframe):
		# rows 0-2, cols 0-5 size 1x3
		self.date_received_input(mainframe)
		self.place_of_origin_input(mainframe)
		self.donation_id_input(mainframe)
		# rows 0-2. cols 6-9 size 3x3
		# self.embed_logo(mainframe)
		# rows 0-2, cols 10-14 size 1x3
		self.technician_input(mainframe)
		self.priority_client_input(mainframe)
		self.autofill_today_in_date(mainframe)
		self.back_button(mainframe)

		self.make_separator_at_row(4)

		self.ask_for_number_of_HDDS(mainframe)
		self.start_time = time.time()

	# HDD Info Frame Rows 3+
	def ask_for_number_of_HDDS(self, f):
		self.num_hdd_label = tk.Label(f, text="Count total number of drives: ")
		self.num_hdd_entry = tk.Entry(f, width=0)
		self.num_hdd_label.grid(row=5, column=0)
		self.num_hdd_entry.grid(row=5, column=3, columnspan=12, sticky='ew')

		self.num_hdd_enter_btn = tk.Button(f, text="Start", width=0)
		self.num_hdd_enter_btn["command"] = lambda: self.generate_input(self.num_hdd_entry.get(), f)
		self.num_hdd_enter_btn.grid(row=6, column=2, columnspan=10, sticky='ew', pady=20)

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
		self.size_input(self.NUM_HDDS, f)
		self.interface_input(self.NUM_HDDS, f)
		self.make_separator_at_row((self.NUM_HDDS+7))
		# Run / Clear Button / Status bar
		self.status_bar(self.NUM_HDDS, f)
		self.run_button(self.NUM_HDDS, f)
		self.clear_errors_button(self.NUM_HDDS, f)

		self.mainframe.bind_all("<MouseWheel>", self.onMouseWheel)

	# GUI has field for Date Received
	def date_received_input(self, f):
		self.date_received_label = tk.Label(f, text="Date Received: ")
		self.date_received_entry = tk.Entry(f)
		self.date_received_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
		self.date_received_entry.grid(row=1, column=3, columnspan=3, padx=5, pady=5)

	# GUI has field for Place of Origin
	def place_of_origin_input(self, f):
		self.place_of_origin_label = tk.Label(f, text="Place of Origin: ")
		self.place_of_origin_entry = tk.Entry(f)
		self.place_of_origin_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
		self.place_of_origin_entry.grid(row=2, column=3, columnspan=3, padx=5, pady=5)

	# GUI has field for Donation ID
	def donation_id_input(self, f):
		self.donation_id_label = tk.Label(f, text="Donation ID: ")
		self.donation_id_entry = tk.Entry(f)
		self.donation_id_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
		self.donation_id_entry.grid(row=3, column=3, columnspan=3, padx=5, pady=5)

	# Adding a personal touch
	def embed_logo(self, f):
		self.logo = tk.PhotoImage(file=resource_path("img/hitlogo.gif"))
		self.logo_label = tk.Label(f, image=self.logo)
		self.logo_label.grid(row=0, column=7, rowspan=3, columnspan=3)


	# GUI has ENTRY for technician which calls the ec.validate_technician function
	def technician_input(self, f):
		
		self.technician_input_label = tk.Label(f, text="Technician: ")
		# Add a grid

		options = {
		'Preston Wong',
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
		
		self.menu.grid(row = 1, column = 12)

		self.technician_input_label.grid(row=1, column=8, columnspan=3, padx=(150, 5), pady=5)
		self.func(self.variable)
		# self.technician_input_entry.grid(row=0, column=11, columnspan=3, padx=5, pady=5)	

	def func(self, value):
		self.technician_input_entry = self.variable.get()
		self.technician = self.technician_input_entry
		print("tech entry", self.technician_input_entry)

	# GUI has a checkbox for priority client
	def priority_client_input(self, f):
		self.priority_client_bool = tk.IntVar()

		self.priority_client_label = tk.Label(f, text="Priority Client: ")
		self.priority_client_entry = tk.Checkbutton(f, variable=self.priority_client_bool)
		self.priority_client_label.grid(row=2, column=8, columnspan=3, padx=(150, 5), pady=5)
		self.priority_client_entry.grid(row=2, column=11, columnspan=3, padx=5, pady=5)

	# GUI autofills today's date
	def autofill_today_in_date(self, f):
		self.autofill_today_label = tk.Label(f, text="Today's Date: ")
		self.autofill_today_date = tk.Label(f, text=datetime.datetime.now().strftime("%m/%d/%y"))
		self.autofill_today_label.grid(row=3, column=8, columnspan=3, padx=(150, 5), pady=5)
		self.autofill_today_date.grid(row=3, column=11, columnspan=3, padx=5, pady=5)


	## This part will have more application logic ##
	## Input has a header designating three fields:
	### barcode, interface, size
	## When enter is pressed, a new field is generated
	## There is an option to autofill based on a parameter up top

	def make_separator_at_row(self, r):
		ttk.Separator(self.mainframe ,orient=tk.HORIZONTAL).grid(row=r, column=0, columnspan=14, sticky='ew', pady=20)

	# GUI has field for GUI barcodes
	def barcode_input(self, num_hdds, f):
		self.barcodes_container = []

		for i in range(num_hdds):
			self.l = tk.Label(f, text="Serial Number: ")
			self.e = tk.Entry(f, width=0)
			self.l.grid(row=i+6, column=0)
			self.e.grid(row=i+6, column=1, columnspan=6, sticky='ew')
			self.barcodes_container.append([self.e, 0])

	# GUI has field ~corresponding to each barcode~ for Gigabyte Size
	def size_input(self, num_hdds, f):
		self.size_container = []

		for i in range(num_hdds):
			self.l = tk.Label(f, text="Capacity: ")
			self.e = tk.Entry(f, width=0)
			self.l.grid(row=i+6, column=7)
			self.e.grid(row=i+6, column=8, columnspan=2, sticky='ew')
			self.size_container.append([self.e, 0])

	# GUI has field ~corresponding to each barcode~ for SATA/SAS Interface
	def interface_input(self, num_hdds, f):
		self.interface_container = []

		for i in range(num_hdds):
			self.interface = tk.StringVar()
			self.interface.set("SATA")

			self.a = tk.Radiobutton(f, variable=self.interface, text="SATA", indicatoron=0, value="SATA")
			self.a.grid(row=i+6, column=10)
			self.b = tk.Radiobutton(f, variable=self.interface, text="SSD", indicatoron=0, value="SSD")
			self.b.grid(row=i+6, column=11)
			self.c = tk.Radiobutton(f, variable=self.interface, text="SAS", indicatoron=0 ,value="SAS")
			self.c.grid(row=i+6, column=12)
			self.c = tk.Radiobutton(f, variable=self.interface, text="EWASTE", indicatoron=0 ,value="EWASTE")
			self.c.grid(row=i+6, column=13)

			self.interface_container.append(self.interface)

	#creates back button interface
	def back_button(self,f):
		self.back_button = tk.Radiobutton(f, text="Back", indicatoron=0, value="Back", padx = 50, command = lambda : self.main_menu(f))
		self.back_button.grid(row=0, column=0)

	#Caleed from ONLY the back button
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

	#USED FOR BACK BUTTON in main_menu
	def start_this_programs(self, true_if_inv, true_if_cert, parent):
		if true_if_inv:
			run_gui(parent)
		elif true_if_cert:
			cc.run_gui(parent)
		else:
			di.run_gui(parent)	
	


	# Called by the run button
	# Makes various calls to functions in error_check.py
	# I have a variable in the error check module called STOP_PARSING
	def run_logic(self):
		# Checks for blank boxes in vendor info
		if ec.check_vendor_blanks(
				self.date_received_entry, self.date_received_entry.get(), 
				self.place_of_origin_entry, self.place_of_origin_entry.get(),
				self.donation_id_entry, self.donation_id_entry.get(),
		):
			self.warning = WarningPopup("You left something blank")
			self.wait_window(self.warning)
			return
		# technician check
		# if not ec.STOP_PARSING:
		# 	self.technician = ec.validate_technician(self.technician_input_entry, self.technician_input_entry)
		# 	print(technician_input_entry)
		# 	if self.technician == "None":
		# 		self.p = WarningPopup("Technician not found. Please check your spelling")
		# 		self.wait_window(self.p)
		if not ec.STOP_PARSING:
			# Checking the date
			self.date_window = ec.parse_date(self.date_received_entry.get(), self.date_received_entry, self.autofill_today_date["text"])
			if self.date_window is not None:
				self.wait_window(self.date_window)
		# Second count of hard-drives NO NEED
		# if not ec.STOP_PARSING:
		# 	self.validationPopup = ValidationPopup("Recount the number of hard-drives to confirm", self.NUM_HDDS)
		# 	self.wait_window(self.validationPopup)
		if not ec.STOP_PARSING:
			# Barcode check in error_check module
			for item in self.barcodes_container:
				item[1] = item[0].get()
			ec.parse_barcodes(self.barcodes_container, self)
		if not ec.STOP_PARSING:
			# HDD Size check in error_check module
			for item in self.size_container:
				item[1] = item[0].get()
			ec.parse_hdd_size(self.size_container, self.interface_container, self)
		if not ec.STOP_PARSING:
			# Priority Client Check
			if self.priority_client_bool.get()==1:
				self.warning = WarningPopup("Be sure to process these PRIORITY CLIENT hard-drives together")
				self.wait_window(self.warning)
				self.priority_client_entry["bg"] = "red"

		if ec.STOP_PARSING:
			ec.STOP_PARSING = False
		else:
			
			#logic to start the logging
			self.p = PromptPopup("Final Confirmation",
				"Push to Asana and Google Sheets?",
				[
				["YES PROCEED", lambda: self.api_hooks(self.p)],
				["NO CANCEL", lambda: self.dummy(self.p)],
				]
				)
			self.wait_window(self.p)
			
	def dummy(self, top):
		print("Dummy function")
		top.destroy()

	def api_hooks(self, top):
		top.destroy()

		self.priority = "False"
		if self.priority_client_bool.get()== 1:
			self.priority = "True"

		self.pack_data()

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

	def kill_program(self, p):
		self.quit()
		p.destroy()

	def pack_data(self):
		#I'm going to pack up the data real nice here
		self.automatic_inventory = []

		for item in self.barcodes_container:
			self.automatic_inventory.append(
				[
					datetime.datetime.now().strftime("%m/%d/%y"), 
					self.date_received_entry.get(), 
					self.place_of_origin_entry.get(),
					self.donation_id_entry.get(),
					self.technician,
					self.priority,
					item[1], # index 6, HDD barcode
					None, # index 7, HDD size
					None, # index 8, HDD interface
					"True"
				]
				)

		for index, item in enumerate(self.size_container):
			self.automatic_inventory[index][7] = str(item[1])

		self.num_inventoried_drives = 0
		self.num_ewasted_drives = 0

		for index, item in enumerate(self.interface_container):
			if item.get() == "EWASTE":
				self.num_ewasted_drives += 1
			else:
				self.num_inventoried_drives += 1
			self.automatic_inventory[index][8] = item.get()

	def push_asana(self, top):
		self.technician = self.technician_input_entry		
		print(self.technician)
		self.start_status(self.NUM_HDDS)
		ashook.main(self.automatic_inventory, top, self.priority, self, self.technician)

	def make_log(self, top):
		# Also uses automatic_inventory from pack_data function
		self.finish_status()
		self.automatic_program_log = [[
			"SUCCESS", 
			str(datetime.datetime.now()), 
			str(self.NUM_HDDS), 
			self.technician, 
			str(round(time.time() - self.start_time, 2)), 
			str(ec.num_errors)
		]]
		print("Time is ",str(round(time.time() - self.start_time, 2)))
		#Now I'm going to call this
		gslog.main(top, self.automatic_inventory, self.automatic_program_log)

	def status_bar(self, HDD, f):
		self.status_bar_label = tk.Label(f, text="Run to Execute")
		self.status_bar_background = tk.Canvas(f, width=500, height=30)
		self.status_bar_background.grid(row=HDD+10, column=0, columnspan=15, sticky='ew')
		self.status_bar_label.grid(row=HDD+11, column=3)
		self.gray_rectangle = self.status_bar_background.create_rectangle(100, 0, 600, 30, fill="grey")


	def run_button(self, HDD, f):
		self.run_button = tk.Button(f, text="Run")
		self.run_button["command"] = lambda: self.run_logic()
		self.run_button.grid(row=HDD+12, column=2, columnspan=5, pady=(20, 20), sticky='ew')

	def clear_errors_button(self, HDD, f):
		self.clear_errors_button = tk.Button(f, text="Clear Errors")
		self.clear_errors_button["command"] = lambda: ec.clear_errors(
			[self.barcodes_container, 
			self.size_container,
			[ 
			[self.date_received_entry, None], 
			[self.place_of_origin_entry, None], 
			[self.donation_id_entry, None],
			[self.technician_input_entry, None],
			], # see ec.clear_errors to see why I did this odd formatting
			])
		self.clear_errors_button.grid(row=HDD+12, column=9, columnspan=4, pady=(20, 20), sticky='ew')

## Below three custom popup classes to call

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

# class ValidationPopup(tk.Toplevel):
# 	def __init__(self, message, NUM_HDDS):
# 		super().__init__()
# 		self.attributes("-topmost", True)
# 		self.focus_force()
# 		self.grab_set()
# 		self.title="Entry Needed"
# 		self.msg = tk.Message(self, text=message)
# 		self.msg.pack()
# 		self.entry = tk.Entry(self)
# 		self.entry.pack()
# 		self.button = tk.Button(self, text="Dismiss", command=lambda: ec.validate_num_hdds(self, self.entry, NUM_HDDS))
# 		self.button.pack()

#I dont knwo what this class does
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

# Called from asana_automate.py
# Constructor that creates the main window object
def run_gui(parent):
	print(resource_path('img/icon.ico'))
	parent.destroy()
	root = tk.Tk()
	root.iconbitmap(resource_path('img/icon.ico'))
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	#root.geometry("{}x{}+0+0".format(w, h))
	root.geometry("{}x{}+0+0".format(850, h-500))
	root.wm_title("Hard Drive Inventory -- Cerebot")
	app = Application(master=root)
	app.pack(side="top", fill="both", expand=True)
	app.mainloop()