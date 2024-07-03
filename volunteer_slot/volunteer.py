import sys,os
from system_configuration.command_line.login_state import *
from view_calendars.view_calendars import *
from view_calendars.download import *
from view_calendars.display_update import *
from view_calendars.file_sytem_setup import *
from system_configuration.command_line.colors.color_decorator import *
from datetime import datetime,timezone
import calendar


def show_code_clinic_slots(user_token_path:str)->int:
    """Shows user code _clinic calendar slots both booked and unbooked
    """
    days = main_view(user_token_path) 
    return days
 
 
def validate_time_input(slot_time)->list: 
    """_summary_

    Args:
        slot_time (_type_): Start time of event givenin format HH:MM and within valid range

    Returns:
        list: a list with boolean values,max number of values being two,each value represents
            validity of HH and MM respectively
    """
    slot_time = slot_time.split(":")
    validity = []
    if len(slot_time) != 2:
        validity = [False,False]
        return validity
     
    if len(slot_time[0]) == 2 and len(slot_time[1]) == 2:
        #Check hours:
        if slot_time[0][0].isdigit() and slot_time[0][1].isdigit():
            if slot_time[0][0] == '0' or slot_time[0][0] == '1':
                #time is between 00:HH and 19:HH
                if 0 <= int(slot_time[0][1])<=9:
                    validity.append(True)
                else:
                    validity.append(False)
                    
            elif slot_time[0][0] == '2':
                if 0 <= int(slot_time[0][1]) < 4:
                    validity.append(True)
                else:
                    validity.append(False)
        
            else:
                validity.append(False)
        else:
            validity.append(False)
            
            
        #Check Minutes
        if slot_time[1][0].isdigit() and slot_time[1][1].isdigit():
            if 0 <= int(slot_time[1][0]) <= 5:
                if 0 <= int(slot_time[1][1]) <= 9:
                    validity.append(True)
                else:
                    validity.append(False)
            else:
                validity.append(False)
        else:
            print(F"{RED}Minute portion not integer value{RESET}")
            validity.append(False)
    else:
        validity=[False,False]

    return validity


def choose_slot(num_days:int,user_email,calendar_id)->datetime:
    """_summary_

    Args:
        events (_type_): _description_
        user_email (_type_): _description_
        calendar_id (_type_): _description_

    Returns:
        datetime: _description_
    """
    vandag = datetime.today()
    last_day = vandag + timedelta(days=num_days)
    slot_day = (input(F"Enter desired day of month in range[{CYAN}{ITALIC}{vandag.year}-{vandag.month}-{vandag.day}{RESET} to  {CYAN}{ITALIC}{last_day.year}-{last_day.month}-{last_day.day}{RESET} MM-DD]:"))
    slot_time = ""
    while not is_slot_day_valid(slot_day,num_days):
        print(F"{YELLOW}Invalid input detected{RESET}")
        slot_day = (input(F"Enter desired day of month in range[{CYAN}{ITALIC}{vandag.year}-{vandag.month}-{vandag.day}{RESET} to  {CYAN}{ITALIC}{last_day.year}-{last_day.month} -{last_day.day}{RESET} MM-DD]:"))
        
    slot_day = slot_day.split("-")   
    slot_time = input(F"Choose a start time for your slot [{CYAN}{ITALIC}HH:MM{RESET}]: ")
    slot_time_split = slot_time.split(":")
    time_validity = validate_time_input(slot_time)
    while False in time_validity:
        time_validity.clear()
        print("Invalid time format,please ensure to input time using HH:MM")
        slot_time = input(F"Choose a start time for your slot [{CYAN}{ITALIC}HH:MM{RESET}]: ")
        time_validity = validate_time_input(slot_time)
        slot_time_split = slot_time.split(":")
        
    slot_date_time = datetime(year=vandag.year, month=int(slot_day[0]), day=int(slot_day[1]), hour=int(slot_time_split[0]), minute=int(slot_time_split[1]), tzinfo=timezone.utc)
    return slot_date_time
    

def is_slot_day_valid(day,num_days)->bool:
    """_summary_

    Args:
        day (_type_): _description_

    Returns:
        bool: _description_
    """
    day = day.strip()
    chosen_day = day.split("-")
    if len(chosen_day) != 2:
        print(F"{YELLOW}No '-' in input{RESET}")
        return False
    
    if chosen_day[0].isdigit() and chosen_day[1].isdigit():
        try:
            vandag = datetime.today()
            vandag = vandag.replace(hour=0, minute=0, second=0, microsecond=0)
            month_range = calendar.monthrange(vandag.year,vandag.month)[1]
            last_day = vandag + timedelta(days=num_days)
            last_day = last_day.replace(hour=23, minute=59, second=59)
            chosen_day = datetime(year=vandag.year, month=int(chosen_day[0]), day=int(chosen_day[1]))
            if vandag <= chosen_day and chosen_day <= last_day:
                return True
            else:
                print(F"{RED}Please choose day within the chosen {num_days+1} days.{RESET}")
                return False
        
        except ValueError:
            print(F"{RED}Invalid month and/or day.{RESET}")
            return False
    
    else:
        print(F"{RED}Month or day not integer value.{RESET}")
        return False
        

def is_slot_available(slot_date_time)->bool:
    """_summary_

    Args:
        slot_date_time (_type_): _description_

    Returns:
        bool: _description_
    """
    data = read_from_csv_file(CALENDAR_DATA_PATH)
    code_clinics_events = []
    for event in data:
        if event["Calendar"] == "code_clinics" or event["Calendar"] == "primary":
            code_clinics_events.append(event)
            
    slot_str = str(slot_date_time)
    slot_split = slot_str.split(" ")
    slot_day = slot_split[0]
    slot_time = slot_split[1].split("+")[0]
    free_slot = True
    for clinic_event in code_clinics_events:
        if clinic_event["Event_Date"] == slot_day:
            if clinic_event["Event_start_time"] == slot_time:
                free_slot = False
                break

    if not free_slot:
        print(F"{BRIGHT_RED}{BOLD}CAN'T BOOK SLOT,AN EVENT IS ALREADY OCCURING AT THAT TIME,PLEASE CHOOSE A DIFFERENT SLOT{RESET}")
        return False
    else:
        return True
    

def confirm_slot(slot_day,slot_time)->bool:
    """Asks user if they want to confirm their slot and returns response as boolean

    Args:
        slot_day (_type_): Date of slot as yyyy-mm-dd
        slot_time (_type_): Start time of slot as HH:MM

    Returns:
        boolean: user's confirmation as bool
    """
    print("Slot Date: ",slot_day,"Slot Start Time: ",slot_time)
    answer = input("Continue with booking?(y/n): ")
    valid_answers = ["y","n"]
    while answer.lower() not in valid_answers:
        answer = input("Continue with booking?(y/n): ")
    if answer.lower() == "y":
        return True
    else:
        print(F"{RED}Booking not confirmed!{RESET}")
        return False
    
 
def make_volunteer_event(user_token_path,start_time:datetime,user_email):
    """Main function for making HTTP request to server and creating a volunteer event
    
    Args:
        user_token_path (_type_): path to the user's token
        start_time (datetime): Date and time of slot in iso format
        user_email (_type_): Currrent User's email address
    """
    user_name = user_email.split("@")
    user_name = user_name[0]
    user_name = user_name.split("023")[0]
    user_name = list(user_name)
    user_name[0] = user_name[0].upper()
    user_name[1] = user_name[1].upper()
    user_name="".join(user_name)
    
    try:
        start_time = start_time-timedelta(hours=2)
        end_time = start_time+timedelta(minutes=30)
        start_time = start_time.isoformat()
        end_time = end_time.isoformat()
        print("Start time -iso: ",start_time,"End time -iso: ",end_time)
        # Book the slot
        service = creds_fetch.create_service("calendar","v3",user_token_path)
        event = {
            'summary': F'{user_name}-Volunteer',
            'description': 'Your additional details here...',
            'start': {'dateTime': start_time, 'timeZone': 'GMT-2:00'},
            'Mbulelo':'all',
            'end': {'dateTime': end_time, 'timeZone': 'GMT-2:00'},
            'attendees':[
                {
                    'email':user_email
                }
            ]
        }

        new_event = service.events().insert(calendarId=code_clinics_id, body=event).execute()
        print(f"{GREEN}Slot booked successfully.{RESET}")
    except HttpError as error:
        print("Volunteering slot fatally failed")
        print("Server returned error response: ",error)
 

def volunteer_initialisation():
    """Prints initialisation message for volunteering in code clinics
    """
    print(F"{MAGENTA}Volunteer your time and expertise to the code clinic{RESET}")


def volunteer_for_slot(user_token_path,user_email):
    """Entry function for module

    Args:
        user_token_path (_type_): File path to user's access token to google api
        user_email (_type_): Email address of user currently logged in 
    """
    volunteer_initialisation()
    days = show_code_clinic_slots(user_token_path)-1
    slot_time = choose_slot(days,".","")
    tries = 10
    while not is_slot_available(slot_time) and tries>1:
        slot_time = choose_slot(days,".","")
        tries -= 1
    
    if not is_slot_available(slot_time):
        print("Failed to choose right slot in 10 tries")
        return
    else:
        slot_str = str(slot_time)
        slot_day = slot_str.split(" ")[0]
        slot_start_time = slot_str.split(" ")[1]
        confirmation = confirm_slot(slot_day,slot_start_time)
        if confirmation:
            make_volunteer_event(user_token_path,slot_time,user_email)
            

if __name__=="__main__":
    volunteer_initialisation()
    show_code_clinic_slots(TOKEN_PATH)
    slot_time=choose_slot(",",".","")
    is_slot_available(slot_time)