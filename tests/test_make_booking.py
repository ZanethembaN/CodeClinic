import unittest
import requests
import re
from datetime import datetime
from unittest.mock import patch
from datetime import date, time

from booking.make_booking import get_booking_date, get_booking_time, check_existing_slot, book_slot


url = "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=894156690185-rmm3ir4un6gmmgj3hk9aelgj4epf3olq.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A47385%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.events&state=xXbPpVg0Oid4tgM2iaEuninEy99cvn&access_type=offline"

class TestBooking(unittest.TestCase):

    @patch('booking.make_booking.get_booking_date',return_value = '2022-02-27')
    def test_valid_currect_year(self,mock_date):
        expected_value = int(mock_date.split("-")[0])
        self.assertTrue(expected_value, datetime.now().year)

    # @patch('booking.make_booking.get_booking_date',return_value = '2024-02-27')
    # @patch('booking.make_booking.get_booking_time',return_value = '13:00:00')
    # def test_date_format(self,mock_date, mock_time):
    #     date_format = r'^\d{4}-\d{2}-\d{2}$'
    #     self.assertTrue(re.match(date_format, mock_date))



    pass

class TestExistingEvent(unittest.TestCase):

    # mock_service = requests.get(url)
    pass
    # @patch('booking.make_booking.get_booking_date',return_value = '2022-02-27')
    # @patch('booking.make_booking.get_booking_time',return_value = '13:00')
    # @patch('view_calendars.download.download_calendar',return_value = [{'Event_Date': '2022-02-27', 'Event_start_time': '13:00', 'Attendees': 'user1@email.com', 'Creator': 'other@email.com'}])
    # def test_check_existing_slot(self,mock_date,mock_time,mock_slots):
    #     # mock_slots = [{'Event_Date': '2022-02-27', 'Event_start_time': '13:00', 'Attendees': 'user1@email.com', 'Creator': 'other@email.com'}]
    #     event_id, booking_date, booking_time = check_existing_slot('token', 'user@email.com')
    #     self.assertEqual((event_id, booking_date, booking_time))


if __name__ == '__main__':
    unittest.main()

