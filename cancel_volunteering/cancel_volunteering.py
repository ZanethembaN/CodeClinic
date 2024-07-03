from datetime import datetime, timedelta
from system_configuration.command_line.colors.color_decorator import *
from system_configuration.command_line.authentication.creds_fetch import create_service
from view_calendars.download import code_clinics_id, download_calendar, get_num_days
from view_calendars.file_sytem_setup import CALENDAR_DATA_PATH
from view_calendars.display_update import (
    write_to_csv, generate_date_and_day, get_current_date, display_pretty_table, read_from_csv_file
)
from googleapiclient.errors import HttpError


def cancel_volunteer_date_valid():
    """
    Validates and returns a user-entered date for cancelling volunteer services.

    Returns:
        datetime.date: Validated user-entered date.
    """

    while True:
        user_volunteering_date = input("Please enter the date you would like to cancel your services (YYYY-MM-DD): ").strip()

        try:
            entered_date = datetime.strptime(user_volunteering_date, "%Y-%m-%d").date()

            current_year = datetime.now().year

            if entered_date < datetime.now().date():
                if entered_date.year != current_year:
                    print(f'{RED}Cannot perform operations for the year {entered_date.year}\nPlease stick to the current year which is {current_year}{RESET}')
                else:
                    print(f"{RED}Date has passed. Please enter an upcoming date.{RESET}")
                continue

            return entered_date

        except ValueError:
            print(f"{RED}Invalid date format. Please use the format YYYY-MM-DD.{RESET}")
            continue


def cancel_volunteer_time_valid(user_path, entered_date, user_email: list) -> str:
    """
    Validates and returns the event ID for cancelling volunteer services.

    Args:
        user_path (str): Path to user data.
        entered_date (datetime.date): Validated user-entered date.
        user_email (list): User email information.

    Returns:
        str: Event ID for the specified date and time.
    """
    user_volunteering_time_str = input(f"Please enter starting time of the event you would like to cancel your services (HH:MM): ").strip()

    try:
        current_hour = datetime.now().hour
        current_min = datetime.now().minute

        user_volunteering_time = datetime.strptime(user_volunteering_time_str, "%H:%M").time()

        if entered_date == datetime.now().date() and (
                user_volunteering_time.hour < current_hour or
                (user_volunteering_time.hour == current_hour and user_volunteering_time.minute <= current_min)
        ):
            print(f"{RED}Cannot input a time that has passed for today.{RESET}")

    except ValueError:
        print(f"{RED}Invalid time format. Please enter your time as HH:MM.{RESET}")

    user_calendar_data = read_from_csv_file(CALENDAR_DATA_PATH)

    for user_data in user_calendar_data:
        if (
            user_data["Event_Date"] == str(entered_date) and
            user_data["Event_start_time"][:-3] == user_volunteering_time_str and
            user_data["Creator"] == user_email[2]
        ):
            event_id = user_data["Event_ID"]
            return event_id

        elif (
            user_data["Event_Date"] == str(entered_date) and
            user_data["Event_start_time"][:-3] == user_volunteering_time_str and not
            user_data["Creator"] == user_email[2]
        ):
            print(f"{RED}{BOLD}Permission not granted. You do not have access to modify this event.{RESET}")
            user_input = input(f"{BOLD}Do you want to choose a different event? (yes/no): ").lower()

            if user_input == 'yes':
                return None
            else:
                return "no"

        elif (
            user_data["Event_Date"] == str(entered_date) and
            user_data["Event_start_time"][:-3] == user_volunteering_time_str and
            user_data["Creator"] == user_email[2] and
            len(user_data["Attendees"])
        ) > 1:
            print(f"{RED}{BOLD}Operation cannot be done; there's already an attendee.{RESET}")
            user_input = input(f"{BOLD}Do you want to choose a different event? (yes/no): ").lower()

            if user_input == 'yes':
                return None
            else:
                break

    print(f"{RED}{BOLD}Invalid time/event found. Please enter a valid time/event as shown on the given calendar!{RESET}")


def can_cancel(user_path, event_id, email):
    """
    Checks if a user has permission to cancel a volunteer event and cancels it if permitted.

    Args:
        user_path (str): Path to user data.
        event_id (str): ID of the event to be cancelled.
        email (str): User email.

    Returns:
        dict or None: Updated event information if cancelled, None otherwise.
    """

    try:
        service = create_service('calendar', 'v3', user_path)

        if service is None:
            print(f"Error: Failed to create Google Calendar service.")
            return None

        try:
            slot = service.events().get(calendarId=code_clinics_id, eventId=event_id).execute()

        except HttpError as e:
            if e.resp.status == 404:
                print(f"{RED}Event not found. Please check the event ID!{RESET}")
            else:
                print(f"HttpError: {e}")
            return None

        num_attendees = len(slot.get("attendees", []))
        event_creator = slot.get("creator", {}).get("email", "")

        email = email[2]

        if email.lower() == event_creator.lower() and num_attendees > 1:
            print(f"{RED}{BOLD}Operation cannot be done; there is already an attendee.{RESET}")
            return None
    

        elif email.lower() == event_creator.lower() and num_attendees == 1:
            print(f"{GREEN}{BOLD}Permission granted. You have access to delete this event.{RESET}")
            confirm_cancel = input(f"{RED}{BOLD}Are you sure you want to cancel the event? (yes/no): {RESET}").lower()

            if confirm_cancel == 'yes':
                slot['summary'] = confirm_cancel
                slot['description'] = f"{confirm_cancel}\nCancelled by: {email}"

                try:
                    updated_slot = service.events().delete(calendarId=code_clinics_id, eventId=event_id).execute()
                    print(f"{GREEN}{BOLD}Event successfully cancelled")

                    print(f"{GREEN}{BOLD}PRESS 'ENTER' TO CONFIRM AND VIEW THE CALENDAR{RESET}")
                    num_days = get_num_days()
                    today_date = get_current_date()
                    day_of_week_date, day_of_week_day = generate_date_and_day(today_date, num_days)
                    events = download_calendar(code_clinics_id, num_days, user_path)
                    write_to_csv(CALENDAR_DATA_PATH, events)
                    display_pretty_table(CALENDAR_DATA_PATH, day_of_week_date, 1)

                    return updated_slot

                except HttpError as e:
                    print(f"Event can't be deleted")
                    return None
            else:
                return None

        else:
            print(f"{RED}{BOLD}Permission denied. You do not have access to delete this event.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main_cancel(user_path, email):
    """
    Main function to initiate the cancellation process for volunteer events.

    Args:
        user_path (str): Path to user data.
        email (str): User email.
    """
    try:
        while True:
            continue_cancellation = 'yes'

            while continue_cancellation == 'yes':
                entered_date = cancel_volunteer_date_valid()
                event_id = cancel_volunteer_time_valid(user_path, entered_date, email)

                if event_id is not None and len(event_id)>5:
                    result = can_cancel(user_path, event_id, email)
                elif event_id == "no":
                    return
                else:
                    break

                continue_cancellation = input(f"{BOLD}Do you want to cancel a different event? (yes/no): ").lower()

            if continue_cancellation == 'no':
                print(f"{CYAN}{BOLD}Goodbye!")
                return

    except Exception as error:
        print(f"An error occurred: {error}")

