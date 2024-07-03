from system_configuration.command_line.colors.color_decorator import *


def say_hello(name):
    """
    The purpose of this function is the 
    welcome greeting
    """

    # ANSI escape code for setting the background colour to blue and text to white
    # initialise_system()
    message = f'{MAGENTA}Hello, {name}{RESET}'
    text = (f"""{CYAN}Welcome to the Code_Clinics Booking System!

We're excited to introduce you to our command-line tools designed to streamline your experience with Code_Clinics.
Whether you're seeking assistance with coding challenges or eager to volunteer your expertise, 
our booking system is here to make the process smooth and efficient.

Thank you for choosing Code_Clinics Booking System! Our team is here to support your coding journey,
so feel free to reach out if you have any questions or need assistance.


Find help for more info!!!


Happy coding!{RESET}""")

    print(message+"\n")
    print(text)


    # return message