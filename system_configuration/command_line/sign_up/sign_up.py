import maskpass
import string
from system_configuration.command_line.authentication.creds_fetch import*
from system_configuration.command_line.colors.color_decorator import *
from view_calendars.file_sytem_setup import *
from system_configuration.command_line.greetings.hello import *


def validate_email(email:str)->bool:
    """
    Function to validate a given email address.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    if email.count("@") != 1:
        return False
    else:
        special_chars = string.punctuation
        email_split = email.split('@')
        if email_split[0] == "":
            return False
        else:
            for char in email_split[0]:
                if char in special_chars:
                    return False
            if email_split[1].lower() != "student.wethinkcode.co.za" or  email_split[1].lower() != "wethinkcode.co.za" :
                return False
        return True


def initilize_user(data):
    """
    Function to initialize a user by obtaining and validating their email and password.

    Args:
        data (list of dicts): A list of dictionaries containing user credentials.

    Returns:
        tuple: A tuple containing the user's email and password if initialization is successful, (None, None) otherwise.
    """
    
    text = """Enter your google email"""
    user_email = input(f"{GREEN}{text}{RESET}: ").lower().strip()
    while not validate_email(user_email):
        print(f"{BRIGHT_YELLOW}Invalid email address{RESET}")
        user_email = input(f"{GREEN}{text}{RESET}: ").lower()

    if user_email in [row['Email'] for row in data]:
        print(f"\n{RED}***User already configured.***\n{RESET}")
        return None, None

    password = maskpass.askpass(f"{GREEN}Enter password: {RESET}").strip()
    verify_password = maskpass.askpass(f"{GREEN}Enter password: {RESET}").strip()      
    while password != verify_password:
        print("Password don't match.Try again!!")
        password = maskpass.askpass(f"{GREEN}Enter password: {RESET}")
        verify_password = maskpass.askpass(f"{GREEN}Enter password: {RESET}") 

    user_token = token_file_name(user_email)
    authenticate_user(user_email,user_token)
    name = user_email.split('@')[0]
    name=list(name)
    name[0]=name[0].upper()
    name[1]=name[1].upper()
    name="".join(name)
    say_hello(name[:-3])

    return user_email,password
