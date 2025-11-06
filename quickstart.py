from datetime import datetime, timezone
import os.path

from PySide6.QtWidgets import QLabel, QApplication
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class calendar:





  def __init__(self):
    super().__init__()


    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    print('authentication verified')

    self.eventlabel0 = QLabel()
    self.eventlabel1 = QLabel()
    self.eventlabel2 = QLabel()
    self.eventlabel3 = QLabel()
    self.eventlabel4 = QLabel()
    self.eventlabel5 = QLabel()
    self.eventlabel6 = QLabel()
    self.eventlabel7 = QLabel()
    self.eventlabel8 = QLabel()
    self.eventlabel9 = QLabel()

    self.timeTill0 = QLabel()
    self.timeTill1 = QLabel()
    self.timeTill2 = QLabel()
    self.timeTill3 = QLabel()
    self.timeTill4 = QLabel()
    self.timeTill5 = QLabel()
    self.timeTill6 = QLabel()
    self.timeTill7 = QLabel()
    self.timeTill8 = QLabel()
    self.timeTill9 = QLabel()
    
    self.pullCalendar(creds)
    self.creds = creds

  
  def pullCalendarMain(self):
      self.pullCalendar(self.creds)


  def pullCalendar(self, creds):

    try:
      service = build("calendar", "v3", credentials=creds)

  
      # Call the Calendar API
      now = datetime.now(timezone.utc)
      nowstr = now.isoformat()
      print("Getting the upcoming 10 events")
      events_result = (
          service.events()
          .list(
              calendarId="skylervarney8112@gmail.com",
              timeMin=nowstr,
              maxResults=10,
              singleEvents=True,
              orderBy="startTime",
          )
          .execute()
      )
      events = events_result.get("items", [])

      eventsList = []

      if not events:
        print("No upcoming events found.")
        return

      #gets the date and name of the next 10 events and appends them to eventList list
      #converts event dictionary ("str","str") to evetnsList list (str str)
      for event in events:
        start = event["start"].get("dateTime", event["start"].get("dateTime"))
        eventsList.append(start + event['summary'])

      

      #fills the event labels with eventList elements which are then sent to button_holder
      eventLabels = [self.eventlabel0, self.eventlabel1, self.eventlabel2, self.eventlabel3, self.eventlabel4, self.eventlabel5, self.eventlabel6, self.eventlabel7, self.eventlabel8, self.eventlabel9]
      timeTill = [self.timeTill0, self.timeTill1, self.timeTill2, self.timeTill3, self.timeTill4, self.timeTill5, self.timeTill6, self.timeTill7, self.timeTill8, self.timeTill9]

      for i, rawEvent in enumerate(eventsList):
        if i < len(eventLabels):

          name = rawEvent[25:]
          eventLabels[i].setText(name)

      for i, rawEvent in enumerate(eventsList):
        if i < len(timeTill):

          start = rawEvent[:19]
          time = self.timeDifference(start)
          timeTill[i].setText(time)


    except HttpError as error:
      print(f"An error occurred: {error}")

  def timeDifference(self, startTime):

    timeFormat = "%Y-%m-%dT%H:%M:%S"
    startTime = datetime.strptime(startTime, timeFormat)
    nowTime = datetime.now()

    timeDifference = startTime - nowTime

    minDifference = timeDifference.total_seconds() / 60
    hourDifference = timeDifference.total_seconds() / 3600
    dayDifference = timeDifference.total_seconds() / 86400

    if dayDifference > 1:
      return "in " + str(round(dayDifference)) + " days"

    elif hourDifference > 1:
      return "in " + str(round(hourDifference)) + " hours"
    
    elif minDifference > 1:
      return "in " + str(round(minDifference)) + " minutes"
    
    else:
      return 'now'
   
    #print(timeDifference)


  
  # [END calendar_quickstart]