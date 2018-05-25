import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import time
import datetime
import error_check as ec
import drive_hook as dh
import asana_hook as ah
import google_sheet_logging as gsl
import os
import sys
import string

from tkinter import *
import graphic_interface as g
import destroy_interface as di

def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
   base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

class Application(tk.Frame):

	def __init__(self, master=None):

		self.master = master

		super().__init__(master)
		self.canvas = tk.Canvas(master, borderwidth=0, background="#005EC4")
		self.mainframe = tk.Frame(self.canvas, background="#fff")
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

	def make_separator_at_row(self, r):
		ttk.Separator(self.mainframe ,orient=tk.HORIZONTAL).grid(row=r, column=0, columnspan=14, sticky='ew', pady=20)

	# Field to do barcode entries, Technician as well
	def populate(self, mainframe):
		self.technician_input(mainframe)
		
		self.make_separator_at_row(1)
		self.back_button(mainframe)
		self.ask_for_number_of_HDDS(mainframe)
		self.start_time = time.time()

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
			run_gui(parent)
		else:
			di.run_gui(parent)	

	def run_logic(self):
		self.num_checked_drives = 0
		self.num_missed_drives = 0
		# Part 1: Error Checking
		# Error checking for blank fields and duplicate fields and missed drives
		# self.technician = ec.validate_technician(self.technician_input_entry.get(), self.technician_input_entry)
		# if self.technician == "None":
		# 	self.p = WarningPopup("Technician not found. Please check your spelling")
		# 	self.wait_window(self.p)
		# Second count of hard-drives
		# if not ec.STOP_PARSING:
		# 	self.validationPopup = ValidationPopup("Recount the number of hard-drives to confirm", self.NUM_HDDS)
		# 	self.wait_window(self.validationPopup)
		if not ec.STOP_PARSING:
			# Barcode check in error_check module
			for item in self.barcodes_container:
				item[1] = item[0].get().strip()
			ec.parse_barcodes(self.barcodes_container, self)

		#CHECK ITEM2
		#if not ec.STOP_PARSING:
			# Barcode check in error_check module
		#	for item2 in self.barcodes_container_2:
		#		item2[1] = item2[0].get().strip()
		#	ec.parse_barcodes(self.barcodes_container_2, self)

		if ec.STOP_PARSING:
			ec.STOP_PARSING = False
			return
		
		
		# Query google drive for barcode given
		for index, item in enumerate(self.barcodes_container):
			self.status_container[index][0]["bg"]="yellow"
			self.status_container[index][0]["text"]="Processing..."
			self.update()
			# Part 2: Cert Checking
			# 2.1 Google drive through Asana
			print("REGULAR SN: ", item[1])
			# deletedFirstSixSN = item[1][6:]
			# print("DELETED FIRST SIX: ", deletedFirstSixSN)

			result = dh.main(item[1])
			# if item[1] == "testCCrdy":
			# 	result = ["Success", None]
			# if item[1] == "testEWrdy":
			# 	result = ["Failed", None]

			# If not found: Update GUI item to Not Found, Make the button red
			if result[0] == "Not Found":
				print("NOT FOUND")
				self.num_missed_drives += 1
				self.status_container[index][0]["bg"]="firebrick1"
				self.status_container[index][0]["text"]="NOT FOUND"

				#CERT CHECKING WITHOUT/WITH PERIOD
				deletingPeriodSerialNumber = item[1].replace('.', '', 1)
				deletedPeriodGoogleDrive = dh.main(deletingPeriodSerialNumber)
				print("deleting period: ", deletingPeriodSerialNumber, ", ", deletedPeriodGoogleDrive)
				if deletedPeriodGoogleDrive[0] == "Not Found":
					self.num_missed_drives += 1
					self.status_container[index][0]["bg"]="firebrick1"
					self.status_container[index][0]["text"]="NOT FOUND"

					deletedFirstSixSN = item[1][6:]
					print("DELETED FIRST SIX: ", deletedFirstSixSN)
					firstSixGoogleDrive = dh.main(deletedFirstSixSN)
					print("working?")
					# self.check = ah.hitachi(item[1], self.technician, False)
					print("First SIX Google drive: ", firstSixGoogleDrive)
					# print("self.check is ", self.check)
					if firstSixGoogleDrive[0] == "Not Found":
						# if self.check == "ERROR":
						print("first non fot found")
						self.num_missed_drives += 1	
						self.status_container[index][0]["bg"]="firebrick1"
						self.status_container[index][0]["text"]="NOT FOUND"

						deletedSecondSixSN = item[1][12:]
						print("DELETED Second SIX: ", deletedSecondSixSN)
						secondSixGoogleDrive = dh.main(deletedSecondSixSN)
						print("SECOND SIX google drive: ", secondSixGoogleDrive)

						# self.check2 = ah.hitachi(item[1], self.technician, False)
						# print("selfcheck2 is: ", self.check2)
						if secondSixGoogleDrive[0] == "Not Found":
						# if self.check2 == "ERROR":
							# if secondSixGoogleDrive[0] == "Not Found":
							self.num_missed_drives += 1
							self.status_container[index][0]["bg"]="firebrick1"
							self.status_container[index][0]["text"]="NOT FOUND"

							print("Before last three: ", item[1])
							deletedLastThree = item[1][:-3]
							print("Last Three deleted", deletedLastThree)
							deletedLastThreeGoogleDrive = dh.main(deletedLastThree)


							if deletedLastThreeGoogleDrive[0] == "Not Found":
								self.num_missed_drives += 1
								self.status_container[index][0]["bg"]="firebrick1"
								self.status_container[index][0]["text"]="NOT FOUND"




							else:
								if deletedLastThreeGoogleDrive[0] == "Failed":
									self.check3 = ah.hitachi(item[1], self.technician, True)
									self.num_checked_drives += 1
									self.status_container[index][0]["bg"]="SteelBlue1"
									self.status_container[index][0]["text"]="FAILED DRIVE"

								if deletedLastThreeGoogleDrive[0] == "Success":
									print("SUccess")
									self.check3 = ah.hitachi(item[1], self.technician, False)
									if self.check3 == "ERROR":
										print("ERROR here!")
										self.num_missed_drives += 1
										self.status_container[index][0]["bg"]="firebrick1"
										self.status_container[index][0]["text"]="NOT FOUND"
									else:
										self.num_checked_drives += 1
										self.status_container[index][0]["bg"]="SeaGreen1"
										self.status_container[index][0]["text"]="SUCCESSFUL WIPE"

						else:
							if secondSixGoogleDrive[0] == "Success":
								self.check2 = ah.hitachi(item[1], self.technician, False)
								if self.check2 == "ERROR":
									self.num_missed_drives += 1
									self.status_container[index][0]["bg"]="firebrick1"
									self.status_container[index][0]["text"]="NOT FOUND"
								else:
									self.num_checked_drives += 1
									self.status_container[index][0]["bg"]="SeaGreen1"
									self.status_container[index][0]["text"]="SUCCESSFUL WIPE"
							if firstSixGoogleDrive[0] == "Failed":
								self.check2 = ah.hitachi(item[1], self.technician, True)
								self.num_checked_drives += 1
								self.status_container[index][0]["bg"]="SteelBlue1"
								self.status_container[index][0]["text"]="FAILED DRIVE"

					else:
						if firstSixGoogleDrive[0] == "Failed":
							self.check = ah.hitachi(item[1], self.technician, True)
							self.num_checked_drives += 1
							self.status_container[index][0]["bg"]="SteelBlue1"
							self.status_container[index][0]["text"]="FAILED DRIVE"
						else:
							self.check = ah.hitachi(item[1], self.technician, False)
							if self.check == "ERROR":
									self.num_missed_drives += 1
									self.status_container[index][0]["bg"]="firebrick1"
									self.status_container[index][0]["text"]="NOT FOUND"
							else:
								self.num_checked_drives += 1
								self.status_container[index][0]["bg"]="SeaGreen1"
								self.status_container[index][0]["text"]="SUCCESSFUL WIPE"
		
		
				else:
					if deletedPeriodGoogleDrive[0] == "Failed":
						self.doublecheck = ah.cert(deletingPeriodSerialNumber, self.technician, True)
						self.num_checked_drives += 1
						self.status_container[index][0]["bg"]="SteelBlue1"
						self.status_container[index][0]["text"]="FAILED DRIVE"

					if deletedPeriodGoogleDrive[0] == "Success":
						self.doublecheck = ah.cert(deletingPeriodSerialNumber, self.technician, False)
						self.num_checked_drives += 1
						self.status_container[index][0]["bg"]="SeaGreen1"
						self.status_container[index][0]["text"]="SUCCESSFUL WIPE"

				#END CERTCHECKING WITHOUT/WITH PERIOD

				

					
			else:
				# Download the file from drive here
				print("Went through else of NOt found")
				print(result)
				dh.main(item[1])
			
				if result[0] == "Failed":
					# Attach the PDF to the Asana Task
					# def cert(s_n, tech, ewaste)
					self.doublecheck = ah.cert(item[1], self.technician, True)
					if self.doublecheck == "ERROR":
						self.num_missed_drives += 1
						self.status_container[index][0]["bg"]="firebrick1"
						self.status_container[index][0]["text"]="NOT FOUND"

						#CERT CHECKING WITHOUT/WITH PERIOD
						deletingPeriodSerialNumber = item[1].replace('.', '', 1)
						self.doublecheck = ah.cert(deletingPeriodSerialNumber, self.technician, True)
						if self.doublecheck == "ERROR":
							self.num_missed_drives += 1
							self.status_container[index][0]["bg"]="firebrick1"
							self.status_container[index][0]["text"]="NOT FOUND"
							# print("Before adding period item1", item[1])
							addingPeriod = item[1] + "."
							# print("Adding Period: ", addingPeriod)
							self.doublecheck = ah.cert(addingPeriod, self.technician, True)
							# print("After add period: ", self.doublecheck)
							if self.doublecheck == "ERROR":
								self.num_missed_drives += 1
								self.status_container[index][0]["bg"]="firebrick1"
								self.status_container[index][0]["text"]="NOT FOUND"
							else:
								self.num_checked_drives += 1
								self.status_container[index][0]["bg"]="SteelBlue1"
								self.status_container[index][0]["text"]="FAILED DRIVE"
						else:
							self.num_checked_drives += 1
							self.status_container[index][0]["bg"]="SteelBlue1"
							self.status_container[index][0]["text"]="FAILED DRIVE"
						#END CERTCHECKING WITHOUT/WITH PERIOD


					else:
					# # FAILED - or SUCCESS with warnings
					# Add a tag "Failed"
					# Move to "Hard Drive Destruction"
					# Add "HDD Ewaste Reason" to "Failed"
					# Update custom fields for technician, method of destruction, date of destruction (today)
					# Update GUI to turn blue
						self.num_checked_drives += 1
						self.status_container[index][0]["bg"]="SteelBlue1"
						self.status_container[index][0]["text"]="FAILED DRIVE"
						
				if result[0] == "Success":
					# def cert(s_n, tech, ewaste)
					self.doublecheck = ah.cert(item[1], self.technician, False)
					print("DoubleCheck: ", self.doublecheck)
					if self.doublecheck == "ERROR":
						print("1")
						self.num_missed_drives += 1
						self.status_container[index][0]["bg"]="firebrick1"
						self.status_container[index][0]["text"]="NOT FOUND"
					
						#CERT CHECKING WITHOUT/WITH PERIOD
						deletingPeriodSerialNumber = item[1].replace('.', '', 1)
						print("Test: ", deletingPeriodSerialNumber)
						self.doublecheck = ah.cert(deletingPeriodSerialNumber, self.technician, False)
						if self.doublecheck == "ERROR":
							print("2")
							self.num_missed_drives += 1
							self.status_container[index][0]["bg"]="firebrick1"
							self.status_container[index][0]["text"]="NOT FOUND"
							# print("Before adding period item1", item[1])
							addingPeriod = item[1] + "."
							# print("Adding Period: ", addingPeriod)
							self.doublecheck = ah.cert(addingPeriod, self.technician, False)
							# print("After add period: ", self.doublecheck)
							if self.doublecheck == "ERROR":
								print("3")
								self.num_missed_drives += 1
								self.status_container[index][0]["bg"]="firebrick1"
								self.status_container[index][0]["text"]="NOT FOUND"
							else:
								self.num_checked_drives += 1
								self.status_container[index][0]["bg"]="SeaGreen1"
								self.status_container[index][0]["text"]="SUCCESSFUL WIPE"
						else:
							self.num_checked_drives += 1
							self.status_container[index][0]["bg"]="SeaGreen1"
							self.status_container[index][0]["text"]="SUCCESSFUL WIPE"
						#END CERTCHECKING WITHOUT/WITH PERIOD

						#LONGEST SERIAL NUMBER (for 2.5 HDDs)
						newTest = item[1][6:]
						print("New Test:", newTest)


						#End longest serial number

					else:
					# # SUCCESS - WIPED HARD DRIVES PROJECT
					# Move to "Wiped Hard Drives" project
					# Change HDD Status to "Wiped"
					# Update GUI to turn green
						self.num_checked_drives += 1
						self.status_container[index][0]["bg"]="SeaGreen1"
						self.status_container[index][0]["text"]="SUCCESSFUL WIPE"
			self.update()
			self.log_array = [
				item[1], 
				str(datetime.datetime.now()), 
				self.technician, 
				result[0],
				(result[0] != "Not Found")
			]
			gsl.cert(self.log_array)
		# Part 3: Success and messaging
		# Display a success message on the amount of drives that were cert checked
		self.p = WarningPopup(
			"Successfully Checked: {} \nHDDS\n\nCould not find: {} \nHDDS\n\n".format(self.num_checked_drives,self.num_missed_drives)
			)
		self.wait_window(self.p)
		# Leave things open so people can double check things

	def ask_for_number_of_HDDS(self, f):
		self.num_hdd_label = tk.Label(f, text="Count total number of drives: ")
		self.num_hdd_entry = tk.Entry(f, width=0)
		self.num_hdd_label.grid(row=2, column=0)
		self.num_hdd_entry.grid(row=2, column=1, columnspan=9, sticky='ew')

		self.num_hdd_enter_btn = tk.Button(f, text="Start", width=0)
		self.num_hdd_enter_btn["command"] = lambda: self.generate_input(self.num_hdd_entry.get(), f)
		self.num_hdd_enter_btn.grid(row=3, column=1, columnspan=8, sticky='ew', pady=20)

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
		# self.deleteLastThree(self.NUM_HDDS, f)
		self.status_input(self.NUM_HDDS, f)
		self.make_separator_at_row((self.NUM_HDDS+7))

		self.run_button(self.NUM_HDDS, f)

		self.mainframe.bind_all("<MouseWheel>", self.onMouseWheel)

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

	def barcode_input(self, num_hdds, f):
	#def barcode_input(self, num_hdds, f, g):
		self.barcodes_container = []
		#self.barcodes_container_2 = []

		for i in range(num_hdds):
			self.l = tk.Label(f, text="Serial Number: ")
			self.e = tk.Entry(f, width=30)
			self.l.grid(row=i+6, column=0)
			self.e.grid(row=i+6, column=1, columnspan=6, sticky='ew', padx=10)
			self.barcodes_container.append([self.e, 0])
			
	def status_input(self, num_hdds, f):
		self.status_container = []

		for i in range(num_hdds):
			self.status_button = tk.Button(f, text="Pending")
			self.status_button["bg"]="peach puff"
			self.status_button.grid(row=i+6, column=9, columnspan=4, sticky='ew')
			self.status_container.append([self.status_button, 0])

	def run_button(self, HDD, f):
		self.run_button = tk.Button(f, text="Run")
		self.run_button["command"] = lambda: self.run_logic()
		self.run_button.grid(row=HDD+12, column=2, columnspan=10, pady=(20, 20), sticky='ew')
	



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


# Constructor that creates the main window object
def run_gui(parent):
	print(resource_path('img/icon.ico'))
	parent.destroy()
	root = tk.Tk()
	root.iconbitmap(resource_path('img/icon.ico'))
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	#root.geometry("{}x{}+0+0".format(w, h))
	root.geometry("{}x{}+0+0".format(750, h-500))
	root.wm_title("Cert Check -- Cerebot")
	app = Application(master=root)
	app.pack(side="top", fill="both", expand=True)
	app.mainloop()