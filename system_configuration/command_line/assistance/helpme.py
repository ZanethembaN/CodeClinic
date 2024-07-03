"""
The purpose of this function
is to provide the list of commands
when you need help.
"""
def need_help():
    print("Run this command 'python3 try.py -help'.\n")

    text = """
    ****************
    Getting Started
    ****************

    Config:
    - Displays user configuration details.
    
    Configuration:
    - Run the configuration tool to set up your connection to WeThinkCode_ and Code Clinic Google calendars.
    - Verify the successful configuration to ensure a seamless experience.

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
    """

    print('List of valid commnad: \n')
    print(text)