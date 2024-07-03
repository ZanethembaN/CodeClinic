import file_sytem_setup
import view_calendars
import sys
import json


if __name__=="__main__":
    arg_list=sys.argv
    valid=["view_calendar","file_setup"]
    if len(arg_list)>1 :
        if arg_list[1].lower() in valid:
            if arg_list[1].lower()=="view_calendar":
                view_calendars.main_view()
            elif arg_list[1].lower()=="file_setup":
                file_sytem_setup.initialise_system()
        else:
            print("unknown command: ",arg_list[1])
            print("type help for info on valid commands")