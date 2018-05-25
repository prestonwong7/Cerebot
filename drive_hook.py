from __future__ import print_function
import httplib2
import os
import sys
import io

from pprint import pprint
from googleapiclient import discovery
from googleapiclient import errors
from googleapiclient.http import MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
   base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'key/client_secret_drive.json'
APPLICATION_NAME = 'Google Drive API Python Quickstart'


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
                                   'drive-python-quickstart.json')

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

# returns status string and link
def main(serial_number=None):
    credentials = get_credentials() # Get credentials with above function
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    # parent_folder_2017 = "" # Deleted for privacy sake
    parent_folder_2017 = "" # ID to searchfor
    # parent_folder_2017 = ""

    # Check for a FAILED DRIVE first
    results = service.files().list(
        pageSize=50,fields="nextPageToken, files(id, name, webViewLink)",
        q="name contains '{}' and fullText contains '{}' and parents='{}'".format(
          serial_number, 'FAILED', parent_folder_2017)).execute()
    items = results.get('files', [])
    if serial_number == '': # if serial number is blank
        return["Not Found", None]
    if items: # if item is found
      download_file(service, items[0]['id']) # use below FUNCTION to downloda
      return ["Failed", items[0]['id']]

    # Check for a FAILED WITH ERRORS DRIVE
    results = service.files().list(
        pageSize=50,fields="nextPageToken, files(id, name)",
        q="name contains '{}' and fullText contains '{}' and parents='{}'".format(
          serial_number, "with warnings", parent_folder_2017)).execute()
    items = results.get('files', []) # initialize item with the above ^ result

    if items: # if item exists
        download_file(service, items[0]['id'])
        return ["Failed", items[0]['id']]


    # Check for a SUCCESS DRIVE
    results = service.files().list(
        pageSize=50,fields="nextPageToken, files(id, name, webViewLink)",
        q="name contains '{}' and fullText contains '{}' and parents='{}'".format(
          serial_number, 'success', parent_folder_2017)).execute()
    items = results.get('files', [])
    if items:
        download_file(service, items[0]['id'])
        return ["Success", items[0]['id']]

    # NOT FOUND
    return ["Not Found", None]

# Downloads file from google drive
def download_file(service, file_id): # uses service? and file ID
    request = service.files().get_media(fileId=file_id) # ? 
    fh = open(resource_path("tmp/cert.pdf"), "wb") # local or remote?
    downloader = MediaIoBaseDownload(fh, request) # ?
    done = False 
    while done is False:
        status, done=downloader.next_chunk() # what happens to status?
        print("Download {}".format(int(status.progress() * 100))) # ? Status

def get_passed(service, parent_folder_2017): # Finds the folder logged inside for successes
    results = service.files().list(pageSize=50, fields="nextPageToken, files(id, name)",
        q="parents='{}' and fullText contains '{}'".format(parent_folder_2017, "success")).execute()
    items = results.get('files', [])
    if not items:
       print('No files found.')
    else:
        for item in items:
            try:
                print('{0} ({1})'.format(item['name'], item['id']))
            except:
                print('{0} ({1})'.format(item['name'], item['id']))
    

def get_failed(service, parent_folder_2017): # Finds folder for failed drives
    results = service.files().list(pageSize=50, fields="nextPageToken, files(id, name)",
        q="parents='{}' and fullText contains '{}'".format(parent_folder_2017, "with warnings")).execute()
    items = results.get('files', [])
    if not items:
       print('No files found.')
    else:
        for item in items:
            try:
                print('Warnings: {0} ({1})'.format(item['name'], item['id']))
            except:
                print('Warnings: {0} ({1})'.format(item['name'], item['id']))

    results = service.files().list(pageSize=50, fields="nextPageToken, files(id, name)",
        q="parents='{}' and fullText contains '{}'".format(parent_folder_2017, "FAILED")).execute()
    items = results.get('files', [])
    if not items:
       print('No files found.')
    else:
        for item in items:
            try:
                print('FAILED:{0} ({1})'.format(item['name'], item['id']))
            except:
                print('FAILED:{0} ({1})'.format(item['name'], item['id']))

def list_all(service, parent_folder_2017, printer=True): # used for what?
    results = service.files().list(pageSize=50, fields="nextPageToken, files(id, name)",
        q="parents='{}'".format(parent_folder_2017)).execute()
    items = results.get('files', [])
    if not items:
       print('No files found.')
    else:
        print('Files:')
        download_file(service, items[0]['id'])
        if printer:
            for item in items:
                try:
                    print('{0} ({1})'.format(item['name'], item['id']))
                except:
                    print('{0} ({1})'.format(item['name'], item['id']))
