import datetime
import re
import calendar
from view_calendars.display_update import read_from_csv_file, write_to_csv
from view_calendars.file_sytem_setup import CALENDAR_DATA_PATH, TOKEN_PATH, CREDENTIALS_PATH
from view_calendars.download import is_up_to_date, get_num_days, code_clinics_id, get_short_calendar_data
from system_configuration.command_line.authentiaction.creds_fetch import create_service
from view_calendars.download import convert_to_time
from tzlocal import get_localzone
import ast



def choose_date():
    while True:
        slot_date = input("Choose date to book a slot (YYYY-MM-DD): ")
        user_time_format = r'\d{4}-\d{2}-\d{2}'
        if re.match(user_time_format, slot_date):
            return slot_date
        else:
            print("Input does not match the specified format.")

def get_current_date():
    now = datetime.datetime.now()
    str_time = now.strftime("%Y-%m-%d %H:%M:%S")
    splitted_str_time = str_time.split()[0]
    year, month, day = map(int, splitted_str_time.split("-"))
    return year, month, day

def last_day_of_month(year, month):
    _, last_day = calendar.monthrange(year, month)
    return last_day

def validate_user_date(year, month, day, last_day, slot_date):
    user_year = int(slot_date[0:4])
    user_month = int(slot_date[5:7])
    user_day = int(slot_date[8:])

    if not (year <= user_year <= year + 1):
        print(f"Invalid year. Please enter a year between {year} and {year + 1}.")
        return False

    if not (1 <= user_month <= 12):
        print(f"Invalid month. Please enter a month between 1 and 12.")
        return False

    if not (1 <= user_day <= last_day):
        print(f"Invalid day. Please enter a day between 1 and {last_day}.")
        return False

    return True

def create_dateTime_object(timestamp, time_format='%Y-%m-%d %H:%M:%S'):
    new = datetime.datetime.strptime(timestamp, time_format)
    return new.isoformat()


def available_slots(user_path):
    num_days = get_num_days()
    is_up_to_date(get_current_date()[2], TOKEN_PATH)
    file_details = read_from_csv_file(CALENDAR_DATA_PATH)

    target_summary = input("Enter the target event summary: ")

    matching_dates = []

    for details in file_details:
        event_description = details["Event_summary"]

        if target_summary in event_description:
            matching_dates.append(details["Event_Date"])

            event_id = details["Event_ID"]
            start_time = details["Event_start_time"]
            end_time = details["Event_end_time"]
            event_date = details["Event_Date"]
            event_attendees = details["Attendees"].split()

            start_time = event_date + " " + start_time
            end_time = event_date + " " + end_time
            start_time = create_dateTime_object(start_time)
            end_time = create_dateTime_object(end_time)

            event_attendees_str = ', '.join(event_attendees)
            new_description = input("New description: ")
            details['Event_summary'] = new_description
            details["Attendees"] = event_attendees
            start_time = details["Event_start_time"]
            end_time = details["Event_end_time"]

            timezone = get_localzone()

            event_body = {
                'summary': new_description,
                'start': {'dateTime': start_time, 'timeZone': str(timezone)},
                'end': {'dateTime': end_time, 'timeZone': str(timezone)},
                'attendees': event_attendees_str
            }

            try:
                write_to_csv(CALENDAR_DATA_PATH, file_details)
                service = create_service("calendar", "v3", user_path)

                print("Event Body:", event_body)

                updated_event = service.events().update(
                    calendarId=code_clinics_id,
                    eventId=event_id,
                    body=event_body
                ).execute()

                print("Slot updated successfully.")
                print("Updated Date:", updated_event['updated'])
            except Exception as e:
                if "Bad Request" in str(e):
                    print("Error updating event: The request was malformed. Please check the event details.")
                else:
                    print(f"Error updating event: {e}")

    if matching_dates:
        print(f"Events with summary '{target_summary}' found on the following dates: {', '.join(matching_dates)}")
    else:
        print(f"No events found with summary '{target_summary}' on the chosen day.")

    return True




def lol(user_path):
    slot_date = choose_date()
    year, month, day = get_current_date()
    last_day = last_day_of_month(year, month)
    if validate_user_date(year, month, day, last_day, slot_date):
        available_slots(user_path)


   