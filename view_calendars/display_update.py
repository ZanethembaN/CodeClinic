import csv
from prettytable import PrettyTable,ALL
from prettytable.colortable import ColorTable,Themes
import datetime
from datetime import date, timedelta
from prettytable import PrettyTable
from prettytable.colortable import ColorTable
from colorama import Fore, Style
from pyfiglet import Figlet
from colors.color_decorator import *

last_date = ''


def write_to_csv(file_path, data):
    """
    Write data to a CSV file.

    Parameters:
    - file_path (str): The path to the CSV file.
    - data (list): A list of dictionaries containing data to be written to the CSV file.

    Returns:
    - list: The input data that was written to the CSV file.
    """
    with open(file_path, 'w', newline='') as write_file:
        fieldnames = ['Event_ID', 'Event_summary', 'Event_Date', 'Event_start_time', 'Event_end_time', 'Attendees',
                      'Creator', 'Calendar',"description", 'last_updated']
        csv_writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)
    return data


def read_from_csv_file(file_path):
    """
    Read data from a CSV file.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - list: A list of dictionaries containing data from the CSV file.
    """
    try:
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data = [row for row in csv_reader]
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


def get_current_date():
    """Gets today's date as a date object

    Returns:
        _type_: date of today
    """
    today_date = date.today()
    return today_date


def day_of_week(date):
    """Gives user day of the week as a three word abbreviation
    Args:
        date (_type_): Date string with YYYY-MM-DD

    Returns:
        str: Day of week abbreviated
    """
    day=datetime.datetime.strptime(date,"%Y-%m-%d").strftime('%a')    
    return day


def display_pretty_table(file_path, day_of_week_date,week_flag):
    """Displays user calendar showing days of the week

    Args:
        file_path (str): _description_
        day_of_week_date (str): _description_
        week_flag (int): _description_
    """
    
    table_label = "Booking System"
    custom_fig = Figlet(font='standard')
    ascii_art = custom_fig.renderText(table_label)
    ascii_art = f'\033[96m{ascii_art}\033[0m'
    print(ascii_art)


    data = read_from_csv_file(file_path)

    if not data:
        print('No data to display')
        return

    set_last_date(day_of_week_date[-1])

    valid_events = filter(is_event_earlier_or_equal, data)
    valid_events = list(valid_events)
    
    columns = day_of_week_date
    days = [day_of_week(d) for d in columns]
    #Get first week
    if week_flag==1:
        columns=columns[:7]
        days = [day_of_week(d) for d in columns]
        
    #Get second week days of the week
    elif week_flag==2:
        columns=columns[7:]
        days = [day_of_week(d) for d in columns]
                
    table = ColorTable()

    new_events = [[] for _ in range(len(columns))]

    for i in range(len(columns)):
        for event in valid_events:
            if event["Event_Date"] == columns[i]:
                summary = f'\033[96m{event["Event_summary"]}\033[0m'
                start1_time = event["Event_start_time"]
                start2_time = start1_time[0:5]
                start3_time = f'\033[90m{"Start"}:\033[0m{start2_time}'
                end1_time = event["Event_end_time"]
                end2_time = end1_time[0:5]
                end3_time = f'\033[90mEnd  :\033[0m{end2_time}'
                new_events[i].append(summary)
                new_events[i].append(start3_time)
                new_events[i].append(end3_time)
                new_events[i].append('-----------------')

    for a in range(len(columns)):
        columns[a] = f"{Fore.LIGHTCYAN_EX}{columns[a]}{Style.RESET_ALL}"
        columns[a] = columns[a] + " " + days[a]

    max_value = max(len(num) for num in new_events)

    empty_list = [[] for _ in range(len(new_events))]

    for x in range(len(empty_list)):
        for y in range(max_value - len(new_events[x])):
            empty_list[x].append('')

    for p in range(len(columns)):
        new_events[p].extend(empty_list[p])

    for count in range(len(columns)):
        if len(new_events[count]) != 0:
            table.add_column(columns[count], new_events[count])
        else:
            table.add_column(columns[count], empty_list[count])

    print(table)


def set_last_date(date):
    """
    Set the global variable 'last_date' to the given date.

    Parameters:
    - date (str): The date to be set as 'last_date'.

    Returns:
    - None
    """
    global last_date
    last_date = convert_to_datetime(date)


def is_event_earlier_or_equal(event: dict):
    """
    Check if the event date is earlier than or equal to the last date.

    Parameters:
    - event (dict): Dictionary representing an event.

    Returns:
    - bool: True if the event date is earlier than or equal to the last date, False otherwise.
    """
    return convert_to_datetime(event["Event_Date"]) <= last_date


def convert_to_datetime(time):
    """
    Convert a string time representation to a datetime object.

    Parameters:
    - time (str): The string representation of time.

    Returns:
    - datetime: A datetime object representing the input time.
    """
    format_str = '%Y-%m-%d'
    formatted_date = datetime.datetime.strptime(time, format_str)
    return formatted_date


def generate_date_and_day(today_date, number_of_days):
    """
    Generate a list of date and day pairs.

    Parameters:
    - today_date (datetime.date): The starting date.
    - number_of_days (int): The number of days to generate.

    Returns:
    - tuple: Lists of date strings and corresponding day strings.
    """
    day_of_week_day = []
    day_of_week_date = []

    for i in range(number_of_days):
        current_date = today_date + timedelta(days=i)
        formatted_date = current_date.strftime("%Y-%m-%d")
        day_of_week = current_date.strftime('%A')

        day_of_week_date.append(formatted_date)
        day_of_week_day.append(day_of_week)
 
    return day_of_week_date, day_of_week_day


def view_free_slots(calendar_path,user_email)->bool:
    """Shows user which slots are available/volunteered for them to book a session 
        Self booking is prohibited and is not possible,so other volunteer's slots will be displayed
    Args:
        calendar_path (str): path to user local calendar file
        user_email (str): user's email address

    Returns:
        bool: returns true if any free slots are available
    """
    data = read_from_csv_file(calendar_path)
    headings = [F"{BRIGHT_GREEN}{BOLD}Volunteer{RESET}",F"{BRIGHT_GREEN}{BOLD}Date{RESET}",F"{BRIGHT_GREEN}{BOLD}Start Time{RESET}",F"{BRIGHT_GREEN}{BOLD}End Time{RESET}"]
    table = ColorTable()
    volunteered_events = [event for event in data if "-Volunteer" in event["Event_summary"] and event["Creator"]!=user_email]
    #print(volunteered_events)
    volunteered_events = sorted(volunteered_events,key=lambda e: e["Event_Date"])
    table.field_names = headings
    table.hrules = ALL
    table.padding_width = 5
    if volunteered_events:
        for evnt in volunteered_events:
            table.add_row([F"{BRIGHT_WHITE}{evnt['Event_summary'].split('-')[0].capitalize()}{RESET}",
                           evnt["Event_Date"],
                           evnt["Event_start_time"],
                           evnt["Event_end_time"]])
        print(F"{BG_BRIGHT_WHITE}{BRIGHT_CYAN}{BOLD}{UNDERLINE}          AVAILABLE SLOTS         {RESET}")
        print(table)
        return True
    else:
        print(F"{RED}No slots available for booking at the moment please try again later{RESET}")
        return False


def view_bookings(calendar_path:str,user_email:str)->bool:
    """Allows user to view bookings they have made with a volunteer

    Args:
        calendar_path (str): path to calendar local file
        user_email (str): user's email address

    Returns:
        bool: Returns true if bookings are found
    """
    data = read_from_csv_file(calendar_path)
    headings=[F"{BRIGHT_GREEN}{BOLD}Booking Details{RESET}",F"{BRIGHT_GREEN}{BOLD}Date{RESET}",F"{BRIGHT_GREEN}{BOLD}Start Time{RESET}",
              F"{BRIGHT_GREEN}{BOLD}End Time{RESET}",F"{BRIGHT_GREEN}{BOLD}Description{RESET}"]
    table=ColorTable()
    volunteered_events=[event for event in data if "booked" in event["Event_summary"] and  user_email in event["Attendees"] and user_email!=event["Creator"]]
    #print(volunteered_events)
    volunteered_events=sorted(volunteered_events,key=lambda e: e["Event_Date"])
    table.field_names=headings
    table.hrules=ALL
    table.padding_width=5
    if volunteered_events:
        for evnt in volunteered_events:
            table.add_row([F"{BRIGHT_WHITE}{evnt['Event_summary'].split('-')[0].capitalize()}{RESET}",
                           evnt["Event_Date"],
                           evnt["Event_start_time"],
                           evnt["Event_end_time"],
                           evnt["description"]])
        print(F"{BG_BRIGHT_WHITE}{BRIGHT_CYAN}{BOLD}{UNDERLINE}         MY BOOKINGS          {RESET}")
        print(table)
        return True
    else:
        print(F"{RED}{BOLD}You have no slots booked at the moment please try again later{RESET}")
        return False
   
    
def view_my_slots(calendar_path:str,user_email:str)->bool:
    """Allows user to view the slots that they have volunteered for

    Args:
        calendar_path (str): path to calendar local file
        user_email (str): user's email address

    Returns:
        bool: returns True if any events were discovered,False otherwise
    """
    data = read_from_csv_file(calendar_path)
    headings=[F"{BRIGHT_GREEN}{BOLD}Date{RESET}",F"{BRIGHT_GREEN}{BOLD}Start Time{RESET}",
              F"{BRIGHT_GREEN}{BOLD}End Time{RESET}",F"{BRIGHT_GREEN}{BOLD}Description{RESET}",F"{BRIGHT_GREEN}{BOLD}Booked By{RESET}"]
    table=ColorTable()
    volunteered_events=[event for event in data if ("-Volunteer" in event["Event_summary"] or "booked" in event["Event_summary"]) and user_email==event["Creator"]]
    volunteered_events=sorted(volunteered_events,key=lambda e: e["Event_Date"])
    table.field_names=headings
    table.hrules=ALL
    table.padding_width=5
    if volunteered_events:
        for evnt in volunteered_events:
            booker="None"
            
            if len(evnt["Attendees"].split(","))==2:
                booker = evnt["Attendees"].split(",")[1]
                booker = booker.split("@")[0]
                booker = booker.split("023")[0]
                booker=list(booker)
                booker[0]=booker[0].upper()
                booker[1]=booker[1].upper()
                booker = "".join(booker)  
                                
            table.add_row([F"{BRIGHT_WHITE}{evnt['Event_Date']}{RESET}",
                           F"{BRIGHT_WHITE}{evnt['Event_start_time']}{RESET}",
                           F"{BRIGHT_WHITE}{evnt['Event_end_time']}{RESET}",
                           F"{BRIGHT_WHITE}{evnt['description']}{RESET}",
                           F"{BRIGHT_WHITE}{booker}{RESET}"])    
        print(F"{BG_BRIGHT_WHITE}{BRIGHT_CYAN}{BOLD}{UNDERLINE}         MY VOLUNTEERING SLOTS          {RESET}")
        print(table)
        return True
    else:
        print(F"{RED}{BOLD}You have not volunteered for any slots, please volunteer first{RESET}")
        return False
