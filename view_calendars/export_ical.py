import csv
from icalendar import Calendar, Event
from datetime import datetime

def read_csv(csv_path):
    """
    Function to read data from a CSV file.

    Args:
        csv_path (str): The path to the CSV file.

    Returns:
        list: A list containing the data read from the CSV file.
    """
    with open(csv_path, "r") as csv_file:
        data = csv.reader(csv_file)
        next(data)
        return list(data)

def get_event_parameters(data):
    """
    Function to extract event parameters from data.

    Args:
        data (list): A list containing event data.

    Returns:
        list: A list containing tuples of event parameters.
    """
    event_param = []
    for param in data:
        summary = param[1]
        start_date = param[2]
        start_time = param[3]
        end_time = param[4]
        event_param.append((summary, start_date, start_time, end_time))
    return event_param

def add_events_to_calendar(events, ics_path):
    """
    Function to add events to a calendar and save it as an ICS file.

    Args:
        events (list): A list of tuples containing event parameters.
        ics_path (str): The path to save the generated ICS file.
    """
    cal = Calendar() 

    for event in events:
        event_name = event[0]
        date = datetime.strptime(event[1], '%Y-%m-%d')
        start_time = datetime.strptime(event[2], '%H:%M:%S').time()
        end_time = datetime.strptime(event[3], '%H:%M:%S').time()
        start_date = datetime.combine(date, start_time)
        end_date = datetime.combine(date, end_time)

        event = Event()
        event.add("summary", event_name)
        event.add("dtstart", start_date)
        event.add('dtend', end_date)
        cal.add_component(event)

    with open(ics_path, "wb") as ics_file:
        ics_file.write(cal.to_ical())

