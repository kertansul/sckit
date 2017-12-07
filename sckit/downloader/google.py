from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import io
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Kertansul\'s Google Drive API'

def get_credentials( flags=None ):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    
    Inputs:
        Set flags based on http://oauth2client.readthedocs.io/en/latest/source/oauth2client.tools.html
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
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def dwnld_with_id(credentials, file_id, dst_pth):
    """ Download Google Drive file with ID

    Inputs:
        credentials: file given by function get_credentials()
        file_id: target file google drive ID
        dst_pth: place + filename to save the target file
    """
    
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO( dst_pth, 'wb' )
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ( '{} Download {}%.'.format( file_id, int(status.progress() * 100) ) )


if __name__ == '__main__':
   
    """ Run this with client_secret.json for the first time

    See https://developers.google.com/drive/v3/web/quickstart/python for further instructions
    """

    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None
    
    cc = get_credentials(flags)
