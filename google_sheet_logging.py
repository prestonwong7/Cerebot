# This class is used to back up all of the certs/inventory/destroying of hard drives into a google sheet 
# in case of any failed connection or etc.


from __future__ import print_function
import httplib2
import sys
import os

from pprint import pprint
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'key/client_secret_sheet.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
   base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(resource_path(CLIENT_SECRET_FILE), SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def cert(arr):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    """
    # This is the inventory log
    """
    spreadsheet_id = '' # Deleted for privacy sake
    range_ = 'Sheet1!A1:E'
    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'
    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'
    values = []
    values.append(arr)
    value_range_body = {
        'values': values
    }
    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, 
        range=range_, 
        valueInputOption=value_input_option, 
        insertDataOption=insert_data_option, 
        body=value_range_body
        )
    response = request.execute()
    pprint(response)

def main(top, inventory_arr, log_arr):
    """
    BELOW: PROGRAM LOG named Automatic-Program-Log
    https://docs.google.com/spreadsheets/d/1PoSreuvJzTxuOgFfP7S-h1Hp9Z5cw41eFeBWgqez3Pw/edit
    BELOW: INVENTORY LOG named Automatic-Inventory
    https://docs.google.com/spreadsheets/d/14_-1oeDKINWsuFdJSeG6vR7-S2PcvoPTvBDcCzmBYxc/edit

    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    """
    # This is the inventory log
    """
 
    spreadsheet_id = '' # Deleted for privacy sake
    range_ = 'Sheet1!A1:J'
    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'
    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'
    values = [
    ]
    for item in inventory_arr:
        values.append(item)
    value_range_body = {
        'values': values
    }
    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, 
        range=range_, 
        valueInputOption=value_input_option, 
        insertDataOption=insert_data_option, 
        body=value_range_body
        )
    response = request.execute()
    pprint(response)

    """
    # This is the program log
    """
    spreadsheet_id = '' # Deleted for privacy sake
    range_ = 'Sheet1!A1:F'
    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'
    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'
    values = log_arr
    value_range_body = {
        'values': values
    }
    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, 
        range=range_, 
        valueInputOption=value_input_option, 
        insertDataOption=insert_data_option, 
        body=value_range_body
        )
    response = request.execute()
    pprint(response)


    top.destroy()