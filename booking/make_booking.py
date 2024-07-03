import datetime
from system_configuration.command_line.colors.color_decorator import *
from view_calendars.download import *
# from view_calendars import download
from view_calendars import display_update
from system_configuration.command_line.authentication.creds_fetch import *

s = "To make a booking"
s1 = "MAKE A BOOKING" 

def get_booking_date(strng = s,strng1 = s1):
    """
    Function to get the desired booking date within the current week.

    Args:
        strng (str): A string representing the prompt message for booking date input.
        strng1 (str): A string representing the prompt message for valid booking date input.

    Returns:
        datetime.date: The booking date chosen by the user.
    """
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    current_date = datetime.date.today()
    max_booking_days = current_date + datetime.timedelta(days=6)

    while True:
        try:
            day = (input(f"{strng}, enter month and day  for the desired slot [{current_year}-MM-DD]: "))
            current_month = int(day.split("-")[0])
            day = int(day.split('-')[1])
            booking_date = datetime.date(current_year, current_month, day) 
            if current_date <= booking_date <= max_booking_days:
                return booking_date
            else:
                print(f"{BRIGHT_YELLOW}{strng1} WITHIN THE CURRENT SEVEN DAYS AS SHOWN IN THE SLOTS TABLE{RESET}")
        except ValueError:
            print(f"{BRIGHT_YELLOW}Enter VALID SLOTS AS SHOWN IN THE AVAILABLE SLOTS TABLE.{RESET}")
        except IndexError:
            print(F'{BRIGHT_YELLOW}INVALID INPUT.{RESET}')


def get_booking_time(booking_date,strng = s):
    """
    Function to get the desired booking time.

    Args:
        booking_date (datetime.date): The booking date chosen by the user.
        strng (str): A string representing the prompt message for booking time input.

    Returns:
        datetime.time: The booking time chosen by the user.
    """
    while True:
        try:
            time_input = input(f"Enter the time for {strng}(HH:MM): ")
            hours, minutes = map(int, time_input.split(':'))
            booking_time = datetime.time(hours, minutes)
            if datetime.datetime.combine(booking_date, booking_time) < datetime.datetime.now():
                print(f"{BRIGHT_YELLOW}{s1} WITHIN THE CURRENT SEVEN DAYS AS SHOWN IN THE SLOTS TABLE{RESET}")
            else:
                return booking_time
        except ValueError:
            print(f"{BRIGHT_YELLOW}INVALID TIME FORMAT. PLEASE ENTER TIME IN{RESET}  {BRIGHT_BLUE}[HH:MM]{RESET} {BRIGHT_YELLOW}FORMAT.{RESET}")

def check_existing_slot(user_token_path,email):
    """
    Function to check for existing slots and validate new bookings.

    Args:
        user_token_path (str): Path to the user token for authentication.
        email (str): User's email address for identification.

    Returns:
        tuple: A tuple containing the event ID, booking date, and booking time if the slot is available and meets the criteria.
    """
    booking_date = get_booking_date(strng = s,strng1 = s1)
    booking_time = get_booking_time(booking_date,s)
    slots = download_calendar(code_clinics_id, 7, user_token_path)

    for slot in slots:
        attendees = slot['Attendees'].split(',')
        num_of_attendees = len(attendees)
      
        if slot["Event_Date"] == str(booking_date) and slot["Event_start_time"] == str(booking_time) :
                if num_of_attendees < 2 and slot['Creator'] != email:
                    event_slot_calendar_id = slot["Event_ID"]
                    return event_slot_calendar_id,booking_date,booking_time

def book_slot(existing_slot_id,user_token_path,email,booking_date,booking_time):
    """
    Function to book a slot.

    Args:
        existing_slot_id (str): The ID of the existing slot.
        user_token_path (str): Path to the user token for authentication.
        email (str): User's email address for identification.
        booking_date (datetime.date): The booking date chosen by the user.
        booking_time (datetime.time): The booking time chosen by the user.

    Returns:
        dict: A dictionary containing the details of the updated booking slot.
    """
    user_name = email.split('@')[0]

    try:
        service = create_service('calendar','v3',user_token_path)

        existing_slot = service.events().get(calendarId=code_clinics_id, eventId=existing_slot_id).execute()

        event_description = input("What is the purpose of your booking: ")  

        confirm_booking = input("Are you sure you want make  a booking at this slot?(y/n): ")

        if confirm_booking.lower() == 'y':
            existing_slot['description'] = event_description

            existing_slot['attendees'].append({'email': email}) 

            slot_summary_edit = existing_slot['summary'].split('-')
            existing_slot['summary'] = f'{slot_summary_edit[0]} booked by {user_name[:-3]}'

            updated_slot = service.events().update(calendarId=code_clinics_id, eventId=existing_slot_id, body=existing_slot, sendUpdates='all').execute()
    
            num_days = 7
            data = download_all(num_days,user_token_path)
            display_update.write_to_csv(file_sytem_setup.CALENDAR_DATA_PATH,data)
            print("confirmed booking for ",booking_date, "at", booking_time,"event_id is",existing_slot_id,".")
            return updated_slot

        elif confirm_booking.lower() not in "yn" or confirm_booking.lower() == "yn":
            print(f"{BRIGHT_RED}INVALID INPUT.BOOKING CANCELLED FIND HELP FOR MORE INFO.{RESET}")
            exit()
        else:
            print("BOOKING CANCELLED FIND HELP FOR MORE INFO.")
            exit()

    except Exception as error:
        print(f"An error occurred: {error}")
