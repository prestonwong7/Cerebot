import sys
import os
import json
from pprint import pprint

import asana

# "I think this class is to test all of asana functions, not used in cerebot anywhere" - Preston

def make_log(result):
	with open(os.path.join(os.getcwd(), 'log/asana_query.txt'), "w") as log_file:
		log_file.write(json.dumps(result, indent=4))
	log_file.close()

def display_all_tags(client, workspace_id):
	tags = client.tags.find_by_workspace(workspace_id)
	pprint(list(tags))
	make_log(list(tags))

def get_all_tasks_within_project(client, project_id):
	tasks = client.tasks.find_by_project(project_id)
	pprint(list(tasks))
	make_log(list(tasks))

def display_all_custom_fields(client, workspace_id):
	custom_fields = client.custom_fields.find_by_workspace(workspace_id)
	pprint(list(custom_fields))
	make_log(list(custom_fields))

def test_complete_a_task(client, task_id):
	result = client.tasks.update(task_id, {"completed":"true"})
	pprint(result)

def find_task_in_project_by_sn(client, project_id, s_n):
	tasks = client.tasks.find_by_project(project_id)
	for task in list(tasks):
		if task['name']==s_n:
			print(task['id'])

# This one is funky because some projects have odd characters
def display_all_projects(client, workspace_id):
	projects = client.projects.find_all({'workspace' : workspace_id})
	make_log("Projects:\n")
	with open(os.path.join(os.getcwd(), 'log/asana_query.txt'), "a") as log_file:
		for p in list(projects):
			try:
				print(p)
				log_file.write(json.dumps(p, indent=4))
			except:
				print("ERROR")
				log_file.write(json.dumps(p, indent=4))

# This one
def display_all_teams(client, workspace_id):
	teams = client.teams.find_by_organization(workspace_id)
	pprint(list(teams))
	make_log(list(teams))

def main():
	# API settings
	# deleted for privacy sake
	token='' # This is my token don't use it to mess anything up please!!!
	client = asana.Client.access_token(token)
	asana.Client.DEFAULTS['page_size'] = 100
	# Getting the test project ID
	workspaces = client.workspaces.find_all()
	# workspace_id = list(workspaces)[0]['id']
	#HDD_Project = 261637939221337
	#WIPED_Project = 114056248943135
	#SAMPLE_ATTACH_ID = 310583477887224
	#READY_TO_WIPE_PROJECT = 261552400938928
	#find_task_in_project_by_sn(client, READY_TO_WIPE_PROJECT, "BJA3P8102HN7")
	display_all_custom_fields(client, workspace_id)
	#result = client.attachments.find_by_task(SAMPLE_ATTACH_ID)
	#result = client.attachments.find_by_id(319142967462967)
	#pprint((result))


if __name__ == "__main__":
	main()

# custom field { Donation ID: 215976511602589 }

# logistics and operations team {'id': 271612690469122, 'name': 'Logistics, Operations'},