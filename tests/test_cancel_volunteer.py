# import unittest
# from datetime import datetime, timedelta
# from unittest.mock import patch
# from cancel_volunteering.cancel_volunteering import (
#     # get_default_date,
#     # get_default_time,
#     # get_user_calendar_last_date,
#     cancel_volunteer_date_valid,
#     cancel_volunteer_time_valid,
#     # check_calendar_slots,
#     can_cancel
# )

# class TestCalendarFunctions(unittest.TestCase):

#     # def test_get_default_date(self):
#     #     result = get_default_date()
#     #     self.assertIsInstance(result, tuple)
#     #     self.assertEqual(len(result), 4)

#     # def test_get_default_time(self):
#     #     result = get_default_time()
#     #     self.assertIsInstance(result, tuple)
#     #     self.assertEqual(len(result), 3)

#     # def test_get_user_calendar_last_date(self):
#     #     current_year_month_date = datetime(2022, 2, 21)
#     #     result = get_user_calendar_last_date(current_year_month_date)
#     #     self.assertIsInstance(result, str)
#     #     self.assertEqual(len(result), 2)

#     @patch('builtins.input', return_value='2024-02-21')
#     def test_cancel_volunteer_date_valid(self, mock_input):
#         current_date = '2024-02-20'
#         calendar_max_date_str = '28'
#         result = cancel_volunteer_date_valid(current_date, calendar_max_date_str)
#         self.assertEqual(result, '2024-02-21')


#     def test_check_calendar_slots(self):
#         user_path = "calendar_data_path"
#         user_volunteering_date = '2024-02-21'
#         user_volunteering_time = datetime.strptime('10:30', '%H:%M')
#         email = 'mero@gmail.com'
#         current_year = '2024'
#         current_month = '02'

#         # result = check_calendar_slots(user_path, user_volunteering_date, user_volunteering_time, email, current_year, current_month)
#         # self.assertIsInstance(result, tuple)
#         # self.assertEqual(len(result), 3)



# if __name__ == '__main__':
#     unittest.main()
