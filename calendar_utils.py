import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']


# Function for Google Calendar Service
def get_google_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


# Function for adding an event to the calendar
def add_event_to_calendar(event_details):
    service = get_google_calendar_service()
    event = {
        'summary': event_details['summary'],
        'start': {'dateTime': event_details['start'], 'timezone': 'UTC'},
        'end': {'dateTime': event_details['end'], 'timezone': 'UTC'},
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return f"Event created: {event.get('htmlLink')}"














