"""
****************
Getting Started
****************

  List of valid commands:

    Config:
    - Displays user configuration details.

    Configuration:
    - Run the configuration tool to set up your connection to WeThinkCode_ and Code Clinic Google calendars.
    - Verify the successful configuration to ensure a seamless experience.

    Login:
    - Allows user to log in to the after configuring to the Code Clinics system.
    - Log in expires after 3 minutes, you have to log in again to continue using the Code Clinics system.

    View Calendars:
    - Explore available time slots by downloading the next 7 days of calendar data.
    - The data will be displayed in an easy-to-read layout on your screen, helping you plan your coding clinic sessions effectively.

    Make a Booking:
    - Reserve your one-on-one coding clinic session by specifying your preferred date, time, and the help you need.
    - Ensure a volunteer is allocated to the slot, and your booking details are updated in our system.

    Volunteer for a Slot:
    - Contribute to the Code_Clinics community by indicating your availability for specific slots.
    - Your volunteering commitment will be reflected in both our system and your personal Google Calendar.

    Cancellation Options:
    - If plans change, you can cancel your booking or volunteering commitment.
    - Note that cancellations are subject to certain conditions to maintain system integrity.


Usage:
    main.py (-h | --help)
    main.py first-run
    main.py sign-up
    main.py login
    main.py config                     
    main.py view-calendar
    main.py view-slots
    main.py view-bookings
    main.py volunteer
    main.py booking
    main.py cancel-volunteer
    main.py cancel-booking
    main.py export-ical
    main.py logout


"""

import sys,os
from docopt import docopt
from system_configuration.command_line.greetings.hello import say_hello
from system_configuration.command_line.leaving.goodbye import say_goodbye
from system_configuration.command_line.assistance.helpme import need_help
from system_configuration.command_line.login.logininfo import *
from system_configuration.command_line.sign_up.sign_up import initilize_user
from system_configuration.command_line.display_data.show_user_config_data import *
from system_configuration.command_line.login_state.log_in_time import *
from system_configuration.command_line.authentication.creds_fetch import *
from system_configuration.command_line.colors.color_decorator import *
from view_calendars.download import *
from view_calendars.view_calendars import *
from view_calendars.file_sytem_setup import *
from view_calendars.export_calendar import *
from volunteer_slot.volunteer import *
from booking.make_booking import *
from booking.cancel_booking import *
from cancel_volunteering.cancel_volunteering import main_cancel
import sys,os

if __name__ == "__main__":
    arguments = docopt(__doc__, version="1.0")

    data = access_configuration_data()

    if arguments['first-run']:
        initialise_system()

    elif arguments['logout']:
        try:
            with open(LOGIN_STATE_FILE,"r") as file:
                    email = file.readline()
                    email = email.split(",")
                    name = email[2].split('@')[0]
                    name=list(name)
                    name[0]=name[0].upper()
                    name[1]=name[1].upper()
                    name="".join(name)
            if name != "":
                say_goodbye(name[:-3])
            else:
                print("No user is logged in.")
        except IndexError:
            print("No user is logged in.")

    elif arguments['sign-up']:
        try:
            email, pwd = initilize_user(data)
            if email and pwd:
                configuration_file(email,pwd)
                user_path=token_file_name(email)
                num_days = 7
                data = download_all(num_days,user_path)
                display_update.write_to_csv(file_sytem_setup.CALENDAR_DATA_PATH,data)
        except FileNotFoundError:
            print(f"{BRIGHT_YELLOW}PLEASE RUN THE FIRST-RUN COMMAND TO SET UP SYSTEM.{RESET}")

    elif arguments['login']:
        email = login(data)
        if(email!=""):
            expiration_time = time.time() + LOGIN_EXPIRATION_SECONDS
            save_login_state(True, expiration_time,email)
                
    elif arguments['view-calendar']:
        logged_in, expiration_time,email = load_login_state()

        if not logged_in or is_login_expired(logged_in, expiration_time):
            print(F"{RED}AUTHORISATION FAILED,PLEASE LOGIN!!!{RESET}")

        else:
            with open(LOGIN_STATE_FILE,"r") as file:
                email = file.readline()
                email = email.split(",")
                user_path=token_file_name(email[2])
                main_view(user_path)

    elif arguments['export-ical']:
        logged_in, expiration_time,email = load_login_state()

        if not logged_in or is_login_expired(logged_in, expiration_time):
           print(F"{RED}AUTHORISATION FAILED,PLEASE LOGIN!!!{RESET}")
        else:
           with open(LOGIN_STATE_FILE,"r") as file:
                email = file.readline()
                email = email.split(",")
                user_path=token_file_name(email[2])
                main_export(user_path)
        
                
    elif arguments['config']:
        logged_in, expiration_time,email = load_login_state()

        if not logged_in or is_login_expired(logged_in, expiration_time):
            print(F"{RED}AUTHORISATION FAILED,PLEASE LOGIN!!!{RESET}")
        else:
            with open(LOGIN_STATE_FILE,"r") as file:
                email = file.readline()
                email = email.split(",")
            read_one_user_file(email[2])
            print("User already signed up")

    elif arguments["volunteer"]:
        logged_in, expiration_time,email = load_login_state()
        if logged_in and not is_login_expired(logged_in,expiration_time):
            with open(LOGIN_STATE_FILE,"r") as file:
                email = file.readline()
                email = email.split(",")
                user_path=token_file_name(email[2])
                volunteer_for_slot(user_path,email[2])
        else:
            print(F"{RED}AUTHORISATION FAILED,PLEASE LOGIN!!!{RESET}")

    elif arguments["booking"]:
        logged_in, expiration_time,email = load_login_state()

        if not logged_in or is_login_expired(logged_in, expiration_time):
            print(F"{RED}AUTHORISATION FAILED,PLEASE LOGIN!!!{RESET}")
        else:
            with open(LOGIN_STATE_FILE,"r") as file:
                email = file.readline()
                email = email.split(",")
                user_path=token_file_name(email[2])
                slots_available=view_free_slots(file_sytem_setup.CALENDAR_DATA_PATH,email[2])
                if not slots_available:
                    exit()
                try:
                    existing_slot_id,booking_date,booking_time = check_existing_slot(user_path,email[2])
                    update_slot = book_slot(existing_slot_id,user_path,email[2],booking_date,booking_time)
                except TypeError:
                    print(f"{RED}**NO AVAILABLE SLOT ON THE SPECIFIED DATE AND TIME.PLEASE CHECK THE SLOTS TABLE TO GET AVAILABLE SLOTS.**{RESET}")

    elif arguments["cancel-booking"]:
        logged_in, expiration_time,email = load_login_state()

        if not logged_in or is_login_expired(logged_in, expiration_time):
            print(F"{RED}AUTHORISATION FAILED,PLEASE LOGIN!!!{RESET}")
        else:
            with open(LOGIN_STATE_FILE,"r") as file:
                email = file.readline()
                email = email.split(",")
                user_path=token_file_name(email[2])
                bookings_available=view_bookings(CALENDAR_DATA_PATH,email[2])
                if not bookings_available:
                    exit()
                try:
                    existing_slot_id,booking_date,booking_time = get_event_for_cancellation(user_path,email[2])
                    cancel_slot = cancel_booking(existing_slot_id,user_path,email[2],booking_date,booking_time)
                    data=download_all(7,user_path)
                    write_to_csv(CALENDAR_DATA_PATH,data)
            
                except TypeError:
                    print(f"{RED}**NO AVAILABLE SLOT ON THE SPECIFIED DATE AND TIME.PLEASE CHECK THE SLOTS TABLE TO GET AVAILABLE SLOTS.**{RESET}")

    elif arguments["view-bookings"]:
        logged_in, expiration_time,email = load_login_state()

        if not logged_in or is_login_expired(logged_in, expiration_time):
            print(F"{RED}AUTHORISATION FAILED,PLEASE LOGIN!!!{RESET}")
        else:
            
            with open(LOGIN_STATE_FILE,"r") as file:
                email = file.readline()
                email = email.split(",")
                user_path = token_file_name(email[2])
                bookings_available = view_bookings(CALENDAR_DATA_PATH,email[2])
    
    elif arguments["view-slots"]:
        logged_in, expiration_time,email = load_login_state()

        if not logged_in or is_login_expired(logged_in, expiration_time):
            print(F"{RED}AUTHORISATION FAILED,PLEASE LOGIN!!!{RESET}")
        else:
            
            with open(LOGIN_STATE_FILE,"r") as file:
                email = file.readline()
                email = email.split(",")
                user_path = token_file_name(email[2])
                data=download_all(14,user_path)
                write_to_csv(CALENDAR_DATA_PATH,data)
                bookings_available = view_my_slots(CALENDAR_DATA_PATH,email[2])
    elif arguments["cancel-volunteer"]:
        logged_in, expiration_time,email = load_login_state()

        if not logged_in or is_login_expired(logged_in, expiration_time):
            print(F"{RED}{BOLD}AUTHORISATION FAILED,PLEASE LOGIN!!!{RESET}")
        else:
            with open(LOGIN_STATE_FILE,"r") as file:
                email = file.readline()
                email = email.split(",")
                user_path=token_file_name(email[2])
                main_view(user_path)
                main_cancel(user_path, email)
 
                
    
    elif arguments['--help']:
        print(__doc__)