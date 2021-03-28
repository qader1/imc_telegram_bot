from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import re

# the scope of the API is what kind of functions it may use. this scope allows to write and read events
# the code below loads the token and request authorization from the user to access his/her account.
# if you authorized the app it will create a credentials.json file but then you need to use your
# IMC calenderID which you would find in your google calendar settings if you added the calendar there
# OTHERWISE IT WON'T WORK

# the process of running the API isn't very simple. you need to go to google's developer console
# and register your program, activate the API for it and couple of other steps after

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)


def get_schedule(time='week'):
    now = datetime.datetime.utcnow()
    if time == 'week':
        time = (now + datetime.timedelta(days=7)).isoformat() + 'Z'
    elif time == 'today':
        time = now.isoformat() + 'Z'
    elif time == 'tomorrow':
        now, time = (now + datetime.timedelta(days=1)).isoformat() + 'Z'
    elif time == 'all':
        time = None
    # which API which version and pass credentials
    service = build('calendar', 'v3', credentials=creds)
    events_result = service.events().list(calendarId='s53nfh7jkv8qc09mh3j89clf8f4tejmp@import.calendar.google.com',
                                          timeMin=now.isoformat() + 'Z',
                                          timeMax=time,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    result = {}
    if not events:
        return 'No classes in the range. enjoy the off time!'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = start.split('T')[0]
        result.setdefault(start, [])
        summary = re.match(r'.*(\d{2}:\d{2} -.* )\(\d LE\)(.*)', event['summary'])
        if summary is not None:
            summary = summary.group(1) + summary.group(2)
            result[start].append(summary)
    return result


if __name__ == '__main__':
    print(get_schedule('all'))
