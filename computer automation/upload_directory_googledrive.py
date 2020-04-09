from __future__ import print_function
import pickle
import os.path
import glob
import mimetypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

tokenPickleDirectory = 'C:/Users/cdurrans/Downloads/'
directoryWeWantToUpload = 'C:\\Users\\cdurrans\\Documents\\'
directoryName = 'Documents'


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(tokenPickleDirectory+'token.pickle'):
        with open(tokenPickleDirectory+'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenPickleDirectory+'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': directoryName,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    folderID = file.get('id')
    count = 0
    for fname in glob.glob(directoryWeWantToUpload+'*'):
        try:
            file_metadata ={
                'name' : fname[fname.rfind('\\')+1:],
                'parents' : [folderID]
            }
            media = MediaFileUpload(fname,
                                    mimetype = mimetypes.guess_type(fname)[0],
                                    resumable = True)
        
            uploadFile = drive_service.files().create(body=file_metadata,
                                            media_body = media,
                                            fields='id').execute()
            print(fname[fname.rfind('\\')+1:],' uploaded.')
        except Exception as ex:
            print(fname)
            print(ex)
        # count += 1
        # if count > 2:
        #     break

    # # Call the Drive v3 API
    # results = service.files().list(
    #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # items = results.get('files', [])

    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()