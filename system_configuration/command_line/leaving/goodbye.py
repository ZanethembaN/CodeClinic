from system_configuration.command_line.colors.color_decorator import *
from system_configuration.command_line.login_state.log_in_time import *
"""
The purpose of this fuction is to
print goodbye
"""
def say_goodbye(name):
    logout()
    message2 = f"{MAGENTA}Goodbye, {name}{RESET}"
    print(message2)

    return message2

