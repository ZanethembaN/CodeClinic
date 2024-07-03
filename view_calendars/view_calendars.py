#View Calendars main
from view_calendars import download
from view_calendars import display_update
import datetime
from view_calendars import file_sytem_setup

def main_view(user_token_path):
    """_summary_

    Args:
        user_token_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    #Credentials are valid
    num_days=download.get_num_days()
    scroll_sentinel=0
    
    if(not download.is_up_to_date(num_days,user_token_path)):
        data=download.download_all(num_days,user_token_path)
        display_update.write_to_csv(file_sytem_setup.CALENDAR_DATA_PATH,data)
    today_date = display_update.get_current_date()
    day_of_week_date=""
    day_of_week_date, day_of_week_day = display_update.generate_date_and_day(today_date, num_days)
    if num_days>7:
        scroll_sentinel=1
        display_update.display_pretty_table(file_sytem_setup.CALENDAR_DATA_PATH,day_of_week_date,scroll_sentinel) 
        scroll=input("View Next page? (y/n):").lower()
        if scroll == "y":
            scroll_sentinel=2
            display_update.display_pretty_table(file_sytem_setup.CALENDAR_DATA_PATH,day_of_week_date,scroll_sentinel)
            
    else:    
        display_update.display_pretty_table(file_sytem_setup.CALENDAR_DATA_PATH,day_of_week_date,scroll_sentinel)  
    #credentials are invalid
    return num_days


def view_volunteers(user_token_path):
    if(not download.is_up_to_date(7,user_token_path)):
        data=download.download_all(7,user_token_path)
        display_update.write_to_csv(file_sytem_setup.CALENDAR_DATA_PATH,data)
    #display_update.view_volunteered_slots(file_sytem_setup.CALENDAR_DATA_PATH)

       
if __name__== "__main__":
    main_view()
  
  
