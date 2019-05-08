from typing import List
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from cerver.models import Response, Form

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate_and_get_service():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/srv/collect/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service

def apply_operation(form: Form, responses: List[List[Response]]) -> int:
    # Call the Sheets API and create a sheet for the given form
    spreadsheet = {
        'properties': {
            'title': form.name
        }
    }
    service = authenticate_and_get_service()

    values = []

    form_questions = (form.form_questions.all())
    label_row = []
    for question in form_questions:
        label_row.append(str(question))
    values.append(label_row)

    for answers in responses:
        row = []
        for response in answers:
            row.append(response.value)
        values.append(row)

    body = {
        'values': values
    }

    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                    fields='spreadsheetId').execute()
    spreadsheet_id = spreadsheet.get('spreadsheetId')
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        valueInputOption="RAW", range='A1', body=body).execute()

    return responses, ('Updated %d cells' % (result.get('updatedCells')))
