import sys
import os
import json
import datetime
from pprint import pprint
import sys


import asana

def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
   base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

def cert(s_n, tech, ewaste):
	# Deleted for privacy sake
	token_dictionary = {
	'Brian Guayante':'',
	'Qu Chen':'',
	'Hayk Tahmasian':'',
	'Preston Wong':'',
	'James Jack':2,
	'Omar Guzman':'',
	'Patrick Carroll':'',
	'Oscar Manzo':'',
	'AJ':'',
	'Hanli Su':''
	}
	token=token_dictionary[tech]
	client = asana.Client.access_token(token)
	# Getting the test project ID
	workspaces = client.workspaces.find_all()
	workspace_id = list(workspaces)[0]['id']
	projects = client.projects.find_all({'workspace' : workspace_id})
	hdd_ready_to_wipe_id = 261552400938928
	wiped_hard_drives = 114056248943135
	hdd_project_id = 403960078573607
	hdd_destruction_id = 261637939221337
	wiped_tag = 101897870019547
	# Asana Custom Field Dictionary
	inventory_dictionary = {
	'HDD Status':'',
	} 
	ewaste_dictionary = {
	'Date of Destruction':'',
	'Destruction Method':'',
	'HDD Ewaste Reason':'',
	'Technician':'',
	}
	custom_field_dictionary = {
	'Wiped':338027791350847,
	'Failed':338027791350852,
	'Ewaste':338027791350845,
	'Shredded':338027791350841,
	}
	technician_dictionary = {
	'Brian Guayante':261697448344642,
	'Hayk Tahmasian':289955731478084,
	'Qu Chen':261697448344643,
	'Preston Wong':289955731478085,
	'James Jack':340989638757661,
	'Omar Guzman':31235412,
	'Patrick Carroll':394528672277201,
	'Oscar Manzo':452266653889276,
	'AJ':500226516940442,
	'Hanli Su':513603040300980
	}
	# Finding the relevant task by barcode
	# Going to automatically populate some
	for field in client.custom_fields.find_by_workspace(workspace_id):
		for wanted in inventory_dictionary:
			if field['name'].strip() == wanted:
				inventory_dictionary[wanted] = field['id']
		for wanted in ewaste_dictionary:
			if field['name'].strip() == wanted:
				ewaste_dictionary[wanted] = field['id']

	# ATTACHMENT LOGIC
	task_id = None
	tasks = client.tasks.find_by_project(hdd_ready_to_wipe_id)
	for task in list(tasks):
		if task['name']==s_n:
			task_id = task['id']
	if task_id is None:
		return "ERROR"
	fh = open(resource_path("tmp/cert.pdf"), "rb")
	certName = "SN: " + str(s_n) + " - certification"
	result = client.attachments.create_on_task(task_id, fh, certName, file_content_type="application/pdf")

	# Failed drive gets turned into ewaste
	if ewaste:
		client.tasks.add_project(task_id, {'project': hdd_destruction_id})
		result = client.tasks.update(task_id,
			{"completed":"true",
			"custom_fields": {
				inventory_dictionary['HDD Status']:custom_field_dictionary['Ewaste'],
				ewaste_dictionary['Date of Destruction']:datetime.datetime.now().strftime("%m/%d/%y"), #Today
				ewaste_dictionary['Destruction Method']:custom_field_dictionary['Shredded'],
				ewaste_dictionary['HDD Ewaste Reason']:custom_field_dictionary['Failed'],
				ewaste_dictionary['Technician']:technician_dictionary[tech],
				},
			})
	# Sucessful drive gets updated
	else:
		client.tasks.add_project(task_id, {'project': wiped_hard_drives})
		result = client.tasks.update(task_id,
			{"custom_fields": {
				inventory_dictionary['HDD Status']:custom_field_dictionary['Wiped'],
				},
			})
	client.tasks.remove_project(result['id'],
		{
		'project': hdd_ready_to_wipe_id
		})
	# client.tasks.add_comment(result['id'],
	# 	{
	# 		'text':'Cerebot Cert Checked'
	# 	})
	return "Okay"

#This function is used to destroy hard drives, putting them into the hard drive destruction folder
def destroy(s_n, tech, ewaste):
	token_dictionary = {
	'Brian Guayante':'', # deleted tokens for privacy sake
	'Qu Chen':'',
	'Hayk Tahmasian':'',
	'Preston Wong':'',
	'James Jack':,
	'Omar Guzman':'',
	'Patrick Carroll':'',
	'Oscar Manzo':'',
	'AJ':'',
	'Hanli Su':''
	}
	token=token_dictionary[tech]
	client = asana.Client.access_token(token)
	# Getting the test project ID
	workspaces = client.workspaces.find_all()
	workspace_id = list(workspaces)[0]['id']
	projects = client.projects.find_all({'workspace' : workspace_id})
	hdd_ready_to_wipe_id = 261552400938928
	wiped_hard_drives = 114056248943135
	hdd_project_id = 403960078573607
	hdd_destruction_id = 261637939221337
	wiped_tag = 101897870019547
	# Asana Custom Field Dictionary
	inventory_dictionary = {
	'HDD Status':'',
	}
	ewaste_dictionary = {
	'Date of Destruction':'',
	'Destruction Method':'',
	'HDD Ewaste Reason':'',
	'Technician':'',
	}
	custom_field_dictionary = {
	'Wiped':338027791350847,
	'Failed':338027791350852,
	'Ewaste':338027791350845,
	'Shredded':338027791350841,
	}
	technician_dictionary = {
	'Brian Guayante':261697448344642,
	'Hayk Tahmasian':289955731478084,
	'Qu Chen':261697448344643,
	'Preston Wong':289955731478085,
	'James Jack':340989638757661,
	'Omar Guzman':358106749002037,
	'Patrick Carroll':394528672277201,
	'Oscar Manzo':452266653889276,
	'AJ':500226516940442,
	'Hanli Su':513603040300980
	}
	# Finding the relevant task by barcode
	# Going to automatically populate some
	for field in client.custom_fields.find_by_workspace(workspace_id):
		for wanted in inventory_dictionary:
			if field['name'].strip() == wanted:
				inventory_dictionary[wanted] = field['id']
		for wanted in ewaste_dictionary:
			if field['name'].strip() == wanted:
				ewaste_dictionary[wanted] = field['id']

	# ATTACHMENT LOGIC
	task_id = None
	tasks = client.tasks.find_by_project(hdd_ready_to_wipe_id)
	for task in list(tasks):
		if task['name']==s_n:
			task_id = task['id']
	if task_id is None:
		return "ERROR"

	# Failed drive gets turned into ewaste
	client.tasks.add_project(task_id, {'project': hdd_destruction_id})
	result = client.tasks.update(task_id,
		{"completed":"true",
		"custom_fields": {
			inventory_dictionary['HDD Status']:custom_field_dictionary['Ewaste'],
			ewaste_dictionary['Date of Destruction']:datetime.datetime.now().strftime("%m/%d/%y"), #Today
			ewaste_dictionary['Destruction Method']:custom_field_dictionary['Shredded'],
			ewaste_dictionary['HDD Ewaste Reason']:custom_field_dictionary['Failed'],
			ewaste_dictionary['Technician']:technician_dictionary[tech],
			},
		})

	client.tasks.remove_project(result['id'],
		{
		'project': hdd_ready_to_wipe_id
		})
	# client.tasks.add_comment(result['id'],
	# 	{
	# 		'text':'Cerebot Destroyed!'
	# 	})
	return "Okay"



# This function is used for inventorying hard drives
def main(arr, top, priority, parent_gui, tech):
	# API settings
	token_dictionary = {
	'Brian Guayante':1,
	'Hayk Tahmasian':'',
	'Preston Wong':'',
	'James Jack':2,
	'Omar Guzman':'',
	'Patrick Carroll':'',
	'Oscar Manzo':'',
	'AJ':'',
	'Hanli Su':''
	}
	token=token_dictionary[tech]
	client = asana.Client.access_token(token)
	# Getting the test project ID
	workspaces = client.workspaces.find_all()
	workspace_id = list(workspaces)[0]['id']
	projects = client.projects.find_all({'workspace' : workspace_id})
	hdd_project_id = 403960078573607
	hdd_destruction_id = 261637939221337
	hdd_ready_to_wipe_id = 261552400938928
	# Finding Priority Tag
	priority_tag_id = 167411461952271
	for tag in client.tags.find_by_workspace(workspace_id):
		if tag['name'] == 'Priorty Client':
			priority_tag_id = tag['id']
	# Asana Custom Field Dictionary
	inventory_dictionary = {
	'HDD Interface':'',
	'Capacity':'',
	'HDD Status':'',
	'Place of Origin':'',
	'Date Received':'',
	'Donation ID':'',
	'Item Type':'',
	}
	ewaste_dictionary = {
	'Date of Destruction':'',
	'Destruction Method':'',
	'HDD Ewaste Reason':'',
	'Technician':'',
	}
	custom_field_dictionary = {
	'SATA':261459380054304,
	'SAS':261459380054305,
	'SSD':410109898608540,
	'Ready to Wipe / Cert Check':338027791350844,
	'Hard Drive':361573479954335,
	# EWASTE
	'Ewaste':338027791350845,
	'Low Value':338027791350850,
	'Shredded':338027791350841,
	}
	technician_dictionary = {
	'Brian Guayante':261697448344642,
	'Hayk Tahmasian':289955731478084,
	'Preston Wong':289955731478085,
	'James Jack':340989638757661,
	'Omar Guzman':358106749002037,
	'Patrick Carroll':394528672277201,
	'Oscar Manzo':452266653889276,
	'AJ':500226516940442,
	'Hanli Su':513603040300980
	}
	# Going to automatically populate some
	for field in client.custom_fields.find_by_workspace(workspace_id):
		for wanted in inventory_dictionary:
			if field['name'].strip() == wanted:
				inventory_dictionary[wanted] = field['id']
		for wanted in ewaste_dictionary:
			if field['name'].strip() == wanted:
				ewaste_dictionary[wanted] = field['id']

	# Here lies the actual API queries
	if priority == "True":
		for index, item in enumerate(arr):
			#EWASTE
			if item[8] == 'EWASTE':
				result = client.tasks.create_in_workspace(workspace_id,
					{'name':item[6], # HDD barcode
					'tags': [priority_tag_id],
					"completed":"true",
					'projects': [hdd_destruction_id, hdd_project_id], 
					"custom_fields": {
						inventory_dictionary['HDD Status']:custom_field_dictionary['Ewaste'],
						inventory_dictionary['Place of Origin']:item[2],
						inventory_dictionary['Donation ID']:item[3],
						inventory_dictionary['Item Type']:custom_field_dictionary['Hard Drive'],
						inventory_dictionary['Date Received']:item[1],
						ewaste_dictionary['Date of Destruction']:item[0], #Today
						ewaste_dictionary['Destruction Method']:custom_field_dictionary['Shredded'],
						ewaste_dictionary['HDD Ewaste Reason']:custom_field_dictionary['Low Value'],
						ewaste_dictionary['Technician']:technician_dictionary[item[4]],
						},
					})
			#INVENTORY
			else:
				result = client.tasks.create_in_workspace(workspace_id,
					{'name':item[6], # HDD barcode
					'tags': [priority_tag_id],
					"custom_fields": {
						inventory_dictionary['HDD Interface']:custom_field_dictionary[item[8]],
						inventory_dictionary['Capacity']:item[7],
						inventory_dictionary['HDD Status']:custom_field_dictionary['Ready to Wipe / Cert Check'],
						inventory_dictionary['Place of Origin']:item[2],
						inventory_dictionary['Donation ID']:item[3],
						inventory_dictionary['Item Type']:custom_field_dictionary['Hard Drive'],
						inventory_dictionary['Date Received']:item[1],
						},
					'projects': [hdd_ready_to_wipe_id, hdd_project_id]
					})
			parent_gui.update_status(index+1)
			client.tasks.remove_project(result['id'],
				{
				'project': hdd_project_id
				})
			# client.tasks.add_comment(result['id'],
			# 	{
			# 		'text':'Cerebot =)'
			# 	})
	else:
		for index, item in enumerate(arr):
			#EWASTE
			if item[8] == 'EWASTE':
				result = client.tasks.create_in_workspace(workspace_id,
					{'name':item[6], # HDD barcode
					'projects': [hdd_destruction_id, hdd_project_id], 
					"completed":"true",
					"custom_fields": {
						inventory_dictionary['HDD Status']:custom_field_dictionary['Ewaste'],
						inventory_dictionary['Place of Origin']:item[2],
						inventory_dictionary['Donation ID']:item[3],
						inventory_dictionary['Item Type']:custom_field_dictionary['Hard Drive'],
						inventory_dictionary['Date Received']:item[1],
						ewaste_dictionary['Date of Destruction']:item[0], #Today
						ewaste_dictionary['Destruction Method']:custom_field_dictionary['Shredded'],
						ewaste_dictionary['HDD Ewaste Reason']:custom_field_dictionary['Low Value'],
						ewaste_dictionary['Technician']:technician_dictionary[item[4]],
						},
					})
			#INVENTORY
			else:
				result = client.tasks.create_in_workspace(workspace_id,
					{'name':item[6], # HDD barcode
					"custom_fields": {
						inventory_dictionary['HDD Interface']:custom_field_dictionary[item[8]],
						inventory_dictionary['Capacity']:item[7],
						inventory_dictionary['HDD Status']:custom_field_dictionary['Ready to Wipe / Cert Check'],
						inventory_dictionary['Place of Origin']:item[2],
						inventory_dictionary['Donation ID']:item[3],
						inventory_dictionary['Item Type']:custom_field_dictionary['Hard Drive'],
						inventory_dictionary['Date Received']:item[1],
						},
					'projects': [hdd_ready_to_wipe_id, hdd_project_id]
					})
			parent_gui.update_status(index+1)
			client.tasks.remove_project(result['id'],
				{
				'project': hdd_project_id
				})
			# client.tasks.add_comment(result['id'],
			# 	{
			# 		'text':'Cerebot =)'
			# 	})

	
	# Destroys parent popup and closes out the program
	if top:
		top.destroy()
	# Optional success message you can remove
	print("API SUCCESS!!!")

# Used to cert check only the Hitachi hard drives, which are hard drives with special cases of serial numbers 
def hitachi(s_n, tech, ewaste):
	token_dictionary = {
	'Qu Chen':'', # Deletd personal tokens for privacy sake
	'Hayk Tahmasian':'',
	'Preston Wong':'',
	'James Jack':,
	'Omar Guzman':'',
	'Patrick Carroll':'',
	'Oscar Manzo':'',
	'AJ':'',
	'Hanli Su':''
	}
	token=token_dictionary[tech]
	client = asana.Client.access_token(token)
	# Getting the test project ID
	workspaces = client.workspaces.find_all()
	workspace_id = list(workspaces)[0]['id']
	projects = client.projects.find_all({'workspace' : workspace_id})
	hdd_ready_to_wipe_id = 261552400938928
	wiped_hard_drives = 114056248943135
	hdd_project_id = 403960078573607
	hdd_destruction_id = 261637939221337
	wiped_tag = 101897870019547
	# Asana Custom Field Dictionary
	inventory_dictionary = {
	'HDD Status':'',
	} 
	ewaste_dictionary = {
	'Date of Destruction':'',
	'Destruction Method':'',
	'HDD Ewaste Reason':'',
	'Technician':'',
	}
	custom_field_dictionary = {
	'Wiped':338027791350847,
	'Failed':338027791350852,
	'Ewaste':338027791350845,
	'Shredded':338027791350841,
	}
	technician_dictionary = {
	'Brian Guayante':261697448344642,
	'Hayk Tahmasian':289955731478084,
	'Qu Chen':261697448344643,
	'Preston Wong':289955731478085,
	'James Jack':340989638757661,
	'Omar Guzman':31235412,
	'Patrick Carroll':394528672277201,
	'Oscar Manzo':452266653889276,
	'AJ':500226516940442,
	'Hanli Su':513603040300980
	}
	# Finding the relevant task by barcode
	# Going to automatically populate some

	for field in client.custom_fields.find_by_workspace(workspace_id):
		for wanted in inventory_dictionary:
			if field['name'].strip() == wanted:
				inventory_dictionary[wanted] = field['id']
		for wanted in ewaste_dictionary:
			if field['name'].strip() == wanted:
				ewaste_dictionary[wanted] = field['id']

	# ATTACHMENT LOGIC
	task_id = None
	tasks = client.tasks.find_by_project(hdd_ready_to_wipe_id)
	for task in list(tasks):
		# print("task name: ", task['name'], "SN: ", s_n)
		if task['name']==s_n:
			task_id = task['id']
			print("TASK ID", task['name'], " AND: ", task['id'], "SN: ", s_n)
	print("TASKID IS: ", task_id)
	if task_id is None:
		return "ERROR"
	fh = open(resource_path("tmp/cert.pdf"), "rb")
	certName = "SN: " + str(s_n) + " - certification"
	result = client.attachments.create_on_task(task_id, fh, certName, file_content_type="application/pdf")

	# Failed drive gets turned into ewaste
	if ewaste:
		client.tasks.add_project(task_id, {'project': hdd_destruction_id})
		result = client.tasks.update(task_id,
			{"completed":"true",
			"custom_fields": {
				inventory_dictionary['HDD Status']:custom_field_dictionary['Ewaste'],
				ewaste_dictionary['Date of Destruction']:datetime.datetime.now().strftime("%m/%d/%y"), #Today
				ewaste_dictionary['Destruction Method']:custom_field_dictionary['Shredded'],
				ewaste_dictionary['HDD Ewaste Reason']:custom_field_dictionary['Failed'],
				ewaste_dictionary['Technician']:technician_dictionary[tech],
				},
			})
	# Sucessful drive gets updated
	else:
		client.tasks.add_project(task_id, {'project': wiped_hard_drives})
		result = client.tasks.update(task_id,
			{"custom_fields": {
				inventory_dictionary['HDD Status']:custom_field_dictionary['Wiped'],
				},
			})
	client.tasks.remove_project(result['id'],
		{
		'project': hdd_ready_to_wipe_id
		})
	# client.tasks.add_comment(result['id'],
	# 	{
	# 		'text':'Cerebot Cert Checked'
	# 	})
	return "Okay"