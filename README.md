Getting Started

This project provides a command-line interface (CLI) to interact with the Code Clinics system. Below is a list of valid commands along with their descriptions:

    Config:
        Displays user configuration details.

    Configuration:
        Run the configuration tool to set up your connection to WeThinkCode_ and Code Clinic Google calendars.
        Verify the successful configuration to ensure a seamless experience.

    Login:
        Allows the user to log in to the Code Clinics system after configuring.
        Login expires after 30 minutes, requiring the user to log in again to continue using the system.

    View Calendars:
        Explore available time slots by downloading the next n days of calendar data.
        The data will be displayed in an easy-to-read layout on your screen, helping you plan your coding clinic sessions effectively.

    Make a Booking:
        Reserve your one-on-one coding clinic session by specifying your preferred date, time, and the help you need.
        Ensure a volunteer is allocated to the slot, and your booking details are updated in our system.
    
    View Bookings:
        Allows user to see their upcomimg bookings they have made with a volunteer in a simple layout
      
    Volunteer for a Slot:
        Contribute to the Code_Clinics community by indicating your availability for specific slots.
        Your volunteering commitment will be reflected in both our system and your personal Google Calendar.

    Export:
        Creates an ICS file and saves it in Desktop folder for user and stores 30 days of data to it.
        Allowing for easy use with external Calendar applications.
    
    Cancellation Options:
        If plans change, you can cancel your booking or volunteering commitment.
        Note that cancellations are subject to certain conditions to maintain system integrity.

Usage:

    main.py hello <name>
    main.py goodbye <name>
    main.py configuration
    main.py login
    main.py config
    main.py view-calendar
    main.py export-ical
    main.py file-setup
    main.py volunteer
    main.py booking
    main.py cancel-booking
    main.py view-bookings
    main.py (-h | --help)

Requirements

Ensure you have virtual a environment activated:
    Refer to requirements.txt
    Installation using p:
        pip install -r requirements.txt

Feel free to explore these commands to interact with the Code Clinics system effectively!
