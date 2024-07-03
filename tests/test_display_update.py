import unittest
import os
import view_calendars.display_update as display_update
import view_calendars.file_sytem_setup as fs

class MyTestCases(unittest.TestCase):

   

    def test_read_CSV_file(self):
        file_path = "calendar_data.csv"
        data = display_update.read_from_csv_file(fs.CALENDAR_DATA_PATH)
        self.assertTrue(data, f"Failed to read data from CSV file: {file_path}")



    def test_get_current_date(self):
        today_date = display_update.get_current_date()

        self.assertIsInstance(today_date, display_update.date)

    def test_generate_date_and_day(self):
        today_date = display_update.get_current_date()
        date_list, day_list = display_update.generate_date_and_day(today_date, number_of_days=5)

        self.assertEqual(len(date_list), 5)
        self.assertEqual(len(day_list), 5)

    """ def test_display_pretty_table_for_days(self):
        test_data = [
            {'Event_ID': '1', 'Event_summary': 'Test Event 1', 'Event_Date': '2024-01-01'},
            {'Event_ID': '2', 'Event_summary': 'Test Event 2', 'Event_Date': '2024-01-02'},
        ]

        file_path = os.path.join(self.test_dir, 'test_file.csv')
        display_update.write_to_csv_file(file_path, test_data)

        today_date = display_update.get_current_date()
        date_list, _ = display_update.generate_date_and_day(today_date, number_of_days=2)
        display_update.display_pretty_table_for_days(file_path, date_list) """

    def test_set_last_date_and_is_event_earlier_or_equal(self):
        display_update.set_last_date('2024-01-02')
        event1 = {'Event_ID': '1', 'Event_Date': '2024-01-01'}
        event2 = {'Event_ID': '2', 'Event_Date': '2024-01-02'}
        event3 = {'Event_ID': '3', 'Event_Date': '2024-01-03'}

        self.assertTrue(display_update.is_event_earlier_or_equal(event1))
        self.assertTrue(display_update.is_event_earlier_or_equal(event2))
        self.assertFalse(display_update.is_event_earlier_or_equal(event3))


if __name__ == "__main__":
    unittest.main()
