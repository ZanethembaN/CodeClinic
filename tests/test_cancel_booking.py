import unittest
import sys
from io import StringIO
from unittest.mock import patch,Mock
from booking.cancel_booking import *
from view_calendars.download import download_calendar

test_event={"Event_ID":"123abc",

            "Event_summary":"drogo booked by ragnar",
            "Event_Date": "2024-02-29",
            "Event_start_time": "10:00",
            "Event_end_time":"g",
            "Attendees": "drogo023@student.wethinkcode.co.za, ragnar023@student.wethinkcode.co.za",
            "Creator":{"email":"user023@student.wethinkcode.co.za"},
            "Calendar":"code_clinics",
            "description":"your_description",
            "last_updated":"2024-3-29T10:05:13.395Z"
            }

test_server_event={"id":"123abc",
            "summary":"drogo booked by ragnar ",
            "Event_Date": "2024-03-29",
            "Event_start_time": "10:00",
            "Event_end_time":"10:30",
            "attendees": [{"email":"drogo023@student.wethinkcode.co.za"}, 
                        {"email":"ragnar023@student.wethinkcode.co.za"}],
            
            "creator":{"email":"drogo023@student.wethinkcode.co.za"},
            "Calendar":"code_clinics",
            "description":"your_description",
            "last_updated":"2024-2-28T10:05:13.395Z"
            }


class TestGetEventForCancellation(unittest.TestCase):
    @patch('view_calendars.download.download_calendar')
    @patch('booking.cancel_booking.get_booking_date')
    @patch('booking.cancel_booking.get_booking_time')
    def test_get_event_cancellation(self,mock_download_calendar,mock_booking_date,mock_booking_time):
        mock_download_calendar.return_value=test_server_event
        mock_booking_date="2024-03-29"  
        mock_booking_time="10:00"
        result_slot,result_date,result_time = get_event_for_cancellation("default_path","ragnar023@student.wethinkcode.co.za")
                

class TestGetEventForCancellation(unittest.TestCase):
    @patch('view_calendars.download.download_calendar')
    @patch('booking.cancel_booking.get_booking_date')
    @patch('booking.cancel_booking.get_booking_time')
    def test_get_event_cancellation(self,mock_download_calendar,mock_booking_date,mock_booking_time):
        mock_download_calendar.return_value=test_server_event
        mock_booking_date="2024-03-29"  
        mock_booking_time="10:00"
        #result_slot,result_date,result_time = get_event_for_cancellation("default_path","ragnar023@student.wethinkcode.co.za")
                

    def test_event_not_found(self):
        pass

    def test_updating_of_events(self):
         pass

    def test_return_type(self):
        pass


class TestCancelBooking(unittest.TestCase):
    def test_invalid_usertoken_path(self):
        pass

    @patch('sys.stdin', new=StringIO("y"))
    @patch('system_configuration.command_line.authentication.creds_fetch.create_service')
    @patch('google_auth_oauthlib.flow.InstalledAppFlow')
    def test_successful_cancellation(self,mock_installed_appflow, mock_create_service):
        
        # test_email = "ragnar023@student.wethinkcode.co.za"
        # test_event = {"event_id": "123abc", "start_time": "2024-02-29T10:00:00"}

        # mock_execute = Mock(return_value=test_event)
        # mock_event_get = Mock()
        # mock_event_get.execute = mock_execute
        # mock_service = Mock()
        # mock_service.events.return_value.get.return_value = mock_event_get
        # mock_create_service.return_value = mock_service

        # mock_flow_instance = mock_installed_appflow.return_value
        # mock_flow_instance.run_local_server.return_value = None  
    
        # cancelled_slot = cancel_booking("123abc", "path_to_user_token", test_email, "2024-02-29", "10:00")

        pass
    def test_event_not_found(self):
        pass