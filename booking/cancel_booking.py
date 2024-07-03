from system_configuration.command_line.authentication.creds_fetch import *
from view_calendars.download import *
from booking.make_booking import *

s = "To cancel a booking"
s1 = "CANCEL A BOOKING" 

def get_event_for_cancellation(user_token_path,email):
    """
    Function to retrieve the event for cancellation.

    Args:
        user_token_path (str): Path to the user token for authentication.
        email (str): User's email address for identification.

    Returns:
        tuple: A tuple containing the event ID, booking date, and booking time if a booking is found for cancellation.
    """
    booking_date = get_booking_date(strng=s,strng1=s1)
    booking_time = get_booking_time(booking_date,strng=s)
    slots = download_calendar(code_clinics_id, 7, user_token_path)
    
    for slot in slots:
        attendees = slot['Attendees'].split(',')
        num_of_attendees = len(attendees)

        if slot["Event_Date"] == str(booking_date) and slot["Event_start_time"] == str(booking_time) :
                if num_of_attendees == 2 and email in attendees:
                    event_slot_calendar_id = slot["Event_ID"]
                    return event_slot_calendar_id,booking_date,booking_time


#def cancel_booking(existing_slot_id,user_token_path,email,booking_date,booking_time):

def cancel_booking(existing_slot_id,user_token_path,email,booking_date,booking_time):
    """
    Function to cancel a booking slot.

    Args:
        existing_slot_id (str): The ID of the existing slot.
        user_token_path (str): Path to the user token for authentication.
        email (str): User's email address for identification.
        booking_date (datetime.date): The booking date chosen by the user.
        booking_time (datetime.time): The booking time chosen by the user.

    Returns:
        dict: A dictionary containing the details of the cancelled booking slot.
    """
    try:
        service = create_service('calendar','v3',user_token_path)
        existing_slot = service.events().get(calendarId=code_clinics_id, eventId=existing_slot_id).execute()
        cancellation_confirmation = input("Are you sure you want cancel a booking at this slot?(y/n): ")

        if cancellation_confirmation .lower() == "y":
            existing_slot['description'] = 'Your additional details here...'

            for attendee in existing_slot['attendees']:
                if 'email' in attendee and attendee['email'] == email and existing_slot["creator"]["email"] != email:
                    existing_slot['attendees'].remove(attendee)

            slot_summary_edit = existing_slot['summary'].split()
            existing_slot['summary'] = f'{slot_summary_edit[0]}-Volunteer'
            cancelled_booking = service.events().update(calendarId=code_clinics_id, eventId=existing_slot_id, body=existing_slot,sendUpdates="all").execute()

            num_days = 7
            data = download_all(num_days,user_token_path)
            display_update.write_to_csv(file_sytem_setup.CALENDAR_DATA_PATH,data)
            print("booking on",booking_date, " occurring at", booking_time,"cancelled")
            return cancelled_booking
        
        elif cancellation_confirmation.lower() not in "yn" or cancellation_confirmation.lower() == "yn":
            print(f"{BRIGHT_RED}INVALID INPUT.BOOKING CANCELLED FIND HELP FOR MORE INFO.{RESET}")
            exit()
        else:
            print("BOOKING CANCELLED FIND HELP FOR MORE INFO.")
            exit()
            
    except Exception as error:
        print(f"An error occurred: {error}")