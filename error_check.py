import sys
from datetime import datetime
import graphic_interface as g
### Part 2: Error Checking ###

STOP_PARSING = False # This variable is set by the abort() function on an error
num_errors = 0

# # If there is a discrepancy in number of hard drives, throw an error
def validate_num_hdds(top, entry, num_hdds):
	if (num_hdds != int(entry.get())):
		p = g.WarningPopup("WARNING: DISCREPANCY IN HARD DRIVE NUMBER COUNT")
		entry["bg"]="red"
		abort()
		top.destroy()
	top.destroy() # Destroys parent entry popup

#Actually don't need anymore, replaced by dropdown box
technician_list = [
	"Patrick Carroll",
	"Omar Guzman",
	"James Jack",
	"Hayk Tahmasian",
	"Preston Wong",
	"Oscar Manzo",
	"AJ",
	"Hanli Su"
	]

# # Input technician entry value and the GUI field
# def validate_technician(t_value, t_gui):
# 	# Checks if first name matches one of many technicians
# 	for tech in technician_list:
# 		if t_value.lower() == tech.split(' ')[0].lower():
# 			return tech
# 	# If not, throws and error and stops the program
# 	t_gui["bg"] = "red"
# 	abort()
# 	return "None"

# # If there is a problem with the date content/format, throw an error
def parse_date(date_recv, date_gui, curr_date):
	# Check that current date is in #MM-YY-DD format
	try:
		stringy_date = str(datetime.strptime(date_recv, "%m/%d/%y").strftime("%m/%d/%y"))
	except:
		p = g.WarningPopup("ERROR: Check date format. Must be MM/DD/YY")
		date_gui["bg"]="red"
		abort()
		return p
	if (date_recv != stringy_date):
		p = g.WarningPopup("ERROR: Check date format. Must be MM/DD/YY")
		date_gui["bg"]="red"
		abort()
	else:
		# Check that the date received input is before or on current date
		recv_parsed = datetime.strptime(date_recv, "%m/%d/%y")
		curr_parsed = datetime.strptime(curr_date, "%m/%d/%y")
		if recv_parsed > curr_parsed:
			p = g.WarningPopup("ERROR: Date received is in the future.")
			date_gui["bg"]="red"
			abort()
		else:
			return None
	return p

# # Returns True to stop loop if any of these are blank
def check_vendor_blanks(date_gui, date_val, place_gui, place_val, donor_gui, donor_val):
	if date_val == '':
		date_gui["bg"]="red"
		abort()
		return True
	if place_val == '':
		place_gui["bg"]="red"
		abort()
		return True
	if donor_val == '':
		donor_gui["bg"]="red"
		abort()
		return True
	return False

# # Generalized anonymous function for the above function
def check_for_null_field(x_val, x_gui):
	if x_val == '':
		x_gui["bg"]="red"
		return True
	return False
	

# Barcode and Drive Size Validation
# Input is an array that contains 
# 1: reference to the entry GUI object 
# 2: the value of the thing itself
def parse_barcodes(arr, master):
	# Checking for empty barcodes and duplicate barcodes
	error_log=""
	for i, code in enumerate(arr):
		message = ""
		if code[1]=="":
			message="ERROR BLANK on ROW {}".format(i+1)
			abort()
			code[0]["bg"]="red"
		else: # Verify that no duplicate scans of hard drives occurred
			for j in range(i-1, -1, -1):
				if arr[j][1] == code[1]:
					message="DUPLICATE ERROR on ROW {}".format(i+1)
					abort()
					code[0]["bg"]="red"
		if message !="":
			if error_log!="":
				error_log += "\n"
			error_log += message

	# Displays errors if there are any error logs
	if error_log != "":
		p = g.WarningPopup(error_log)
		master.wait_window(p)

# Have to store drive number here because I cannot pass the value to the GUI
# current_drive keeps track of the current index of the drive being error checked for size
# root_master is a reference to the main gui, so that error_check can automagically ewaste drives
current_drive = 0
root_master = None
# Check that the HDD meets the right criteria
def parse_hdd_size(arr, interface_type, master):
	root_master = master
	for index, item in enumerate(arr):
		if interface_type[index].get() != "EWASTE" and item[1] == "":
			p = g.WarningPopup("You left this one blank!")
			item[0]["bg"]="red"
			abort()
			return
		if interface_type[index].get() != "EWASTE" and interface_type[index].get() != "SSD" and int(item[1]) < 140: ## Is it under 140GB? If so...
			current_drive = index
			item[0]["bg"]="red"
			## It must be 80GB Seagate, Western Digital, or a SSD
			# def throw_prompt(title, message, args): takes title, message, and args is a 2d array containing button text and function reference (make this a lambda)
			p = g.PromptPopup( "Size Error",
							"This drive does not meet the minimum specifications for processing. Are you sure this isn't e-waste?",
							[
							# # NOT-EWASTE | EWASTE | ENTRY-MISTAKE
							["NOT-EWASTE", lambda: clear(item[0], p)], # This option just continues
							["EWASTE", lambda: ewaste_drive(interface_type[index], item[0], p)], # This option will switch the field to e-waste
							["ENTRY-MISTAKE", lambda: abort(p)], # This option will stop the script
							]
							)
			master.wait_window(p)

def ewaste_drive(interface_var, entry_gui_item, parent):
	interface_var.set("EWASTE")
	entry_gui_item["bg"]="white"
	parent.destroy()

def abort(parent=None):
	global STOP_PARSING
	STOP_PARSING = True
	global num_errors
	num_errors += 1
	if parent is not None:
		parent.destroy()


def clear(entry_gui_item, parent):
	entry_gui_item["bg"]="white"
	parent.destroy()

# Passed an array of GUI objects containing...
# HDD Barcode Entry
# HDD Size Entry
# Vendor Input Fields
def clear_errors(entry_arrays):
	for arr in entry_arrays:
		for entry in arr:
			entry[0]["bg"]="white"