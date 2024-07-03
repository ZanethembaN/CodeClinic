import os
import time
from view_calendars.file_sytem_setup import LOGIN_STATE

LOGIN_STATE_FILE = LOGIN_STATE
LOGIN_EXPIRATION_SECONDS = 1800  # 30 minutes

def save_login_state(logged_in, expiration_time, email):
    """
    Function to save the login state to a file.

    Args:
        logged_in (bool): Flag indicating whether the user is logged in or not.
        expiration_time (float): The timestamp indicating the expiration time of the login.
        email (str): The user's email address.
    """
    with open(LOGIN_STATE_FILE, "w") as file:
        file.write(f"{logged_in},{expiration_time},{email}")

def load_login_state():
    """
    Function to load the login state from a file.

    Returns:
        tuple: A tuple containing the login status, expiration time, and user's email address.
    """
    if os.path.exists(LOGIN_STATE_FILE):
        with open(LOGIN_STATE_FILE, "r") as file:
            data = file.read().split(',')
            if len(data) == 3:
                logged_in, expiration_time, email = data
                return bool(logged_in), float(expiration_time), str(email)
    return False, 0, ""

def is_login_expired(logged_in, expiration_time):
    """
    Function to check if the login has expired.

    Args:
        logged_in (bool): Flag indicating whether the user is logged in or not.
        expiration_time (float): The timestamp indicating the expiration time of the login.

    Returns:
        bool: True if the login has expired, False otherwise.
    """
    if logged_in:
        current_time = time.time()
        return current_time > expiration_time
    else:
        # If not logged in, treat it as expired
        return True

def logout():
    """
    Function to log out the user by resetting the login state.
    """
    save_login_state(False, 0, '')
