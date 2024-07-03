import datetime
import os.path
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from system_configuration.command_line.authentication import creds_fetch

from view_calendars import file_sytem_setup

code_clinics_id="c_c437f085da8700a680ec190aabdfdc072c2eef6c67fa57350f98068908ba3329@group.calendar.google.com"


def get_num_days()-> int:
    """Prompts user for number of days to be fetched and dislplayed
    if invalid input or no input sets default to 7

    Returns:
       int: number of days
    """
    num_days = (input("Please input number of days to view(default=7,Max=14) :"))
    if num_days == None or not num_days.isnumeric() or int(num_days) <= 0 or int(num_days)>14 :
        print("Invalid input...Setting to default")
        num_days = 7
    return int(num_days)    


def download_calendar(calendar_id:str,num_days:int,user_token_path)->list:
    """fetches list of events from user calendar with the given calendar id
       and limits number of results

    Args:
        calendar_id (str): _description_
        num_days (int): _description_

    Returns:
        list: _description_
    """
    try:
        service = creds_fetch.create_service("calendar","v3",user_token_path)
        if service == None:
            raise ValueError
        
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        last = datetime.datetime.utcnow() + datetime.timedelta(days=num_days)
        last_day = last.isoformat()+"Z"
        primary_events_result = (
            service.events()
            .list(
                calendarId = calendar_id,
                timeMin = now,
                timeMax = last_day,
                singleEvents = True,
                orderBy = "startTime",
            )
            .execute()
        )
        events = primary_events_result.get("items", [])
        if not events:
            if(calendar_id == "primary"):
                print("No upcoming primary events found.")
            else:
                print("No upcoming code clinic events found.")
            return

        event_keys = ("Event_ID","Event_summary","Event_Date","Event_start_time","Event_end_time","Attendees",
                     "Creator","Calendar","description","last_updated")
        events_list =[]
        
        for event in events:
            if "date" in event["start"]:
                start_time="00:00:00"
                end_time="23:59:59"
                date=event["start"]["date"]
            else:
                start_time = event["start"]["dateTime"].split("T")[1]
                date = event["start"]["dateTime"].split("T")[0]
                start_time = start_time.split("+")[0]
                end_time = event["end"]["dateTime"].split("T")[1]
                end_time = end_time.split("+")[0]
            
            attendees = ""
            if("attendees" in event):
                attendants = event["attendees"]
                for attendee in attendants :
                    attendees += attendee["email"]+","
                attendees = (attendees.rstrip(","))
            else:
                pass   
            if(calendar_id != "primary"):
                id = "code_clinics"
            else:
                id = "primary"
            description = "No description"
            if "description" in event:
                description = event["description"]
            
            summary="No Title"
            if "summary"  in event:
                summary= event["summary"]
                
            event_details = (event["id"],summary,date,start_time,end_time,attendees,event["creator"].get("email"),id,description,event["updated"])
            events_list.append(dict(zip(event_keys,event_details)))

        return events_list
    except HttpError as error:
        print(f"An error occurred: {error}")
    except ValueError as error:
        print("Credentials None existent or Invalid")
 
        
def is_up_to_date(num_days:int,user_token_path:str)->bool:
    """Checks local data against online data then returns True if
    local copy is not up to date

    Args:
        num_days (int): Number of days to check against
        user_token_path (str): path to user's token file

    Returns:
        bool: Status of local copy
    """
    local_data = read_local_data()
    online_data = get_short_calendar_data(num_days,user_token_path)
    update_array = []
    update_ids = []
    #Check if all online ID's are present in offline ids
    online_ids = [val["id"] for val in online_data]
    offline_ids = [val["id"] for val in local_data]
    for value in online_ids:
        if value not in offline_ids:
            return False
        
    for item in online_data:
        for item2 in local_data:
            #find matching online_id in local data
            if(item["id"] == item2["id"]):
                #Check if last updated of item matches
                item1_time = convert_to_time(item["updated"])
                item2_time = convert_to_time(item2["updated"])
                if(item1_time == item2_time):
                    update_array.append(False)
                else:
                    update_array.append(True)
                    update_ids.append(item["id"])
    if True in update_array:
        return False
    else:
        return True
    
        
def read_local_data()->list:
    """Reads data from local storage file and returns events as
    list of dictionaries

    Returns:
        list: events as list of dictionaries
    """

    local_data = []
    update_check_headings = ("id","updated")
    with open(file_sytem_setup.CALENDAR_DATA_PATH,'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row_details = (row["Event_ID"],row["last_updated"])
            local_data.append(dict(zip(update_check_headings,row_details)))
    return local_data


def get_short_calendar_data(number_days:int,user_token_path:str)->list:
    """Gets calendar data from google calendar and keeps last_updated and event ID

    Args:
        number_days (int): Number of days from today to fetch events for
        user_token_path (str): path to user token file

    Returns:
        list: events returned as list of dictionaries
    """
    service = creds_fetch.create_service("calendar","v3",user_token_path)
    now = datetime.datetime.utcnow().isoformat() + "Z"
    last = datetime.datetime.utcnow() + datetime.timedelta(days=number_days)
    last_day = last.isoformat()+"Z"
    all_events = []
    headings = ("id","updated")
    try:
        events = service.events().list(calendarId = 'primary',singleEvents = True,timeMin = now,timeMax = last_day).execute()
        for event in events["items"]:
            details=(event["id"],event["updated"])
            all_events.append(dict(zip(headings,details)))
            
        events = service.events().list(calendarId=code_clinics_id,singleEvents=True,timeMin=now,timeMax=last_day).execute()
        for event in events["items"]:
            details = (event["id"],event["updated"])
            all_events.append(dict(zip(headings,details)))

        return(all_events)
    except HttpError as error:
        print("Server returned:",error)

    
def convert_to_time(timestamp)->datetime:
    """Converts a timestamp string to an iso formatted datetime objects

    Args:
        timestamp (str): Date and time timestamp

    Returns:
        datetime: datetime object converted from input
    """
    format = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.datetime.strptime(timestamp,format)    
 
     
def download_all(days:int,user_token_path)->list: 
    """_summary_
    Downloads data from primary and code_clinics calendar
    Then merges everthing into one list

    Args:
        days (int): number of days for which data must be returned

    Returns:
        list: list of events where each event is a dictionary
    """
    all_events = download_calendar("primary",days,user_token_path)
    code_clinic_events = download_calendar(code_clinics_id,days,user_token_path)
    primary_ids = [x["Event_ID"] for x in all_events]
    code_clinic = []
    if code_clinic_events:
        for event in code_clinic_events:
            if event['Event_ID'] not in primary_ids:
                code_clinic.append(event)
                
        all_events.extend(code_clinic)
        
    sorted_events = sorted(all_events,key = lambda x:x["Event_start_time"])
  
    return sorted_events
    

if __name__ == "__main__":
    pass
