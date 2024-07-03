# View Calendars main
from view_calendars import download
from view_calendars import display_update
import datetime
from view_calendars.export_ical import *
from view_calendars.file_sytem_setup import CALENDAR_DATA_PATH, ICAL_DATA_PATH

def main_export(user_token_path):
    """
    Main function to export calendar data to iCal format.

    This function checks if the calendar data is up-to-date, downloads it if necessary,
    writes it to a CSV file, converts the data to iCal format, and saves it as an .ics file.

    Args:
        user_token_path (str): The path to the user token file.

    """
    num_days = 30
    if not download.is_up_to_date(num_days, user_token_path):
        data = download.download_all(num_days, user_token_path)
        display_update.write_to_csv(CALENDAR_DATA_PATH, data)
        try:
            data = read_csv(CALENDAR_DATA_PATH)
            rows = get_event_parameters(data)
            add_events_to_calendar(rows, ICAL_DATA_PATH)
            print("iCal export complete")
            print("File location: ", ICAL_DATA_PATH)
        except StopIteration:
            print("No events to convert to iCal")
