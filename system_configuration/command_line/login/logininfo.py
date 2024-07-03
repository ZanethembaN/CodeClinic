import maskpass #pip install
import smtplib,random
from system_configuration.command_line.colors.color_decorator import *
from system_configuration.command_line.display_data.show_user_config_data import *
from email.message import EmailMessage
from socket import gethostbyname, gaierror

# secret_key = pyotp.random_base32()
# otp = pyotp.TOTP(secret_key).now()
def get_otp():
    """
    Generates a 6-digit OTP (One Time Password).

    Returns:
        str: A string representing the generated OTP.
    """
    random_code_list = random.sample(range(0,9),6)
    otp = ""
    for dig in random_code_list:
        otp += str(dig)
    return otp

def login(data):
    """
    Logs in a user based on provided credentials.

    Args:
        data (list): A list containing user data.

    Returns:
        str: The email address of the logged-in user.
    """
    tries = 0
    max_tries =  3
    while tries < max_tries:
        text = """Enter your google email"""
        email = input(f"{GREEN}{text}{RESET}: ")
        password = maskpass.askpass(f"{GREEN}Enter password:{RESET} ")

        for user in data:

            if user["Email"]==email and user['Password']==password:
                print(f"{GREEN}log in successful!!{RESET}")
                return email

        print(f"\n{BRIGHT_YELLOW}incorrect credentials.log in unsuccessful!!TRY AGAIN.{RESET}\n") 
        tries += 1
    
    pwd = input("forgot password?(y/n) ")

    if pwd.lower() == "y":
        password = reset_password(data)
        edit_configuration_password(data,password)
    else:
        print("please log in.\nPlease configure to use code_clinics\nfind help for more info")


def send_otp(email,data,otp):
    """
    Sends OTP (One Time Password) to the provided email.

    Args:
        email (str): The email address to which OTP will be sent.
        data (list): A list containing user data.
        otp (str): The OTP (One Time Password) to be sent.

    Returns:
        str: The email address to which OTP is sent.
    """
    for user in data:
        if user["Email"]==email:

            text = EmailMessage()
            text.set_content(f"Your OTP token is: {otp}")
            text["Subject"] = 'Code Buddy Password Reset'
            text["From"] = "codebuddy158@gmail.com"
            text["To"] = email

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('codebuddy158@gmail.com', 'ccfo wltr uwga uhrv ')
                smtp.send_message(text)

            print("user configured")
            return email

        else:
            print("user not configured")
 
def verify_otp(otp_input,otp):
    """
    Verifies the input OTP with the generated OTP.

    Args:
        otp_input (str): The OTP entered by the user.
        otp (str): The OTP generated.

    Returns:
        bool: True if OTP input matches the generated OTP, False otherwise.
    """
    if otp_input == otp:
        return True
    return False

def reset_password(data):
    """
    Resets the password for a user after OTP verification.

    Args:
        data (list): A list containing user data.

    Returns:
        str: The new password if reset is successful, None otherwise.
    """
    otp = get_otp()
    email = input("please provide email: ")
    try:
        send_otp(email,data,otp)
    except gaierror:
        print(f"{RED}\nFAILED TO SEND OTP DUE TO INTERNET FAILURE.{RESET}")
        exit()
    otp_input = input("Enter the OTP received in your email: ")

    if verify_otp(otp_input,otp):
        print(f"{GREEN}OTP verification successful. Proceed to access Google Calendar API.{RESET}")
        password = maskpass.askpass(f"{GREEN}Enter password: {RESET}")
        verify_password = maskpass.askpass(f"{GREEN}Confirm password: {RESET}") 
        if password == verify_password:
            return password
        else:
            print(f"{RED}Password dont match{RESET}")
            return None
    else:
        print(f"{RED}OTP verification failed. Access denied.{RESET}")
