
import datetime
from system_configuration.command_line.colors.color_decorator import *
from view_calendars.download import *
from system_configuration.command_line.authentication import *

def get_booking_date():
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    current_date = datetime.date.today()
    max_booking_days = current_date + datetime.timedelta(days=6)

    while True:
        try:
            day = int(input(f"Enter day of month for the desired slot booking: "))
            booking_date = datetime.date(current_year, current_month, day) 
            if current_date <= booking_date <= max_booking_days:
                return booking_date
            else:
                print(f"{RED}Make a booking within the current seven days as shown in the slot table{RESET}")
        except ValueError:
            print(f"Enter valid slot as shown in the available slots.")


def get_booking_time(booking_date):
    while True:
        try:
            time_input = input("Enter the time for the booking (HH:MM): ")
            hours, minutes = map(int, time_input.split(':'))
            booking_time = datetime.time(hours, minutes)
            if datetime.datetime.combine(booking_date, booking_time) < datetime.datetime.now():
                print("Make a booking within the current seven days as shown in the slot table")
            else:
                return booking_time
        except ValueError:
            print("Invalid time format. Please enter the time in HH:MM format.")


def check_existing_slot(user_token_path):

    #print(user_token_path)
    booking_date = get_booking_date()
    booking_time = get_booking_time(booking_date)
    slots = download_calendar(code_clinics_id, 7, user_token_path)
    # slots = []
    #print(booking_date)
    #print(booking_time)
    #print(f"{BOLD}getting avalable slots{RESET}")
    #print(slots)

    #print("Slots:", slots)
    
    # if slots:
    #     for slot in slots:
    #         attendees = slot['Attendees'].split(',') if slot['Attendees'] else []
    #         num_attendees = len(attendees)
            
    #         if slot["Event_Date"] == str(booking_date) and slot["Event_start_time"] == str(booking_time):
    #             if num_attendees == 1:
    #                 print("Slot available.")
    #                 event_description = input("What do you need help with: ")
                    
    #                 slot["Event_summary"] = event_description
    #                 slot["Attendees"] += f"{email}"
    #                 num_days = 7
    #                 download_calendar(code_clinics_id,num_days,user_token_path)
    #                 # display_update.write_to_csv(file_sytem_setup.CALENDAR_DATA_PATH,data)
    #                 print("Event no longer available for booking.")

    #                 print(f"{BOLD}update slot{RESET}",slots)
                    
    #                 print("Booking confirmed for", booking_date, "at", booking_time)
    #                 break
    #             if num_attendees == 2:
    #                 print(f"{RED} slot already booked.{RESET}")
    #                 break
    #         else:
    #             print("No available slots found for the specified date and time.")
    #             break
    # else:
    #     print("No slots available.")

    # if slots:

    for slot in slots:
        attendees = slot['Attendees'].split(',')
        num_of_attendees = len(attendees)
        #print('here in number of guest',num_of_attendees)
        if slot["Event_Date"] == str(booking_date) and slot["Event_start_time"] == str(booking_time) :#and len(slot['Attendees']) <= 2:
                if num_of_attendees < 2:
                    event_slot_calendar_id = slot["Event_ID"]
                    #print(event_slot_calendar_id)
                    return event_slot_calendar_id,booking_date,booking_time

        
def check_slot_availabitity(existing_slot_id,user_token_path,email):

    # print(email)
    user_name = email.split('@')[0]
    service = creds_fetch.create_service('calendar','v3',user_token_path)

    # existing_slot = check_existing_slot(user_token_path)

    existing_slot = service.events().get(calendarId=code_clinics_id, eventId=existing_slot_id).execute()

    event_description = input("What is the purpose of your booking: ")

    existing_slot['description'] = event_description
    # existing_slot['anyoneCanAddSelf'] = True
    existing_slot['attendees'].append({'email': email}) 

    slot_summary_edit = existing_slot['summary'].split('-')
    existing_slot['summary'] = f'{slot_summary_edit[0]}- booked-{user_name}'

    updated_slot = service.events().update(calendarId=code_clinics_id, eventId=existing_slot_id, body=existing_slot).execute()

    print(f"{BOLD}Updating Slot{RESET}")
    #print(updated_slot)
    return updated_slot


def book_slot(updated_slot,booking_date,booking_time):

    confirm_booking = input("Are you sure you want make  a booking at this slot?(YES/NO): ")


    if confirm_booking.upper() == 'YES':
        print("Booking confirmed for", booking_date, "at", booking_time)
        return updated_slot

    else:
        print("Booking cancelled. find help for more info.")



