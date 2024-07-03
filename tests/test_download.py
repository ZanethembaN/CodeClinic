import unittest
import view_calendars.download as download
import sys
from io import StringIO
from unittest.mock import patch

class download_testCase(unittest.TestCase):
    def test_get_num_days(self):
        #Test_Valid input
        sample_days='5'
        with patch("sys.stdin",new=StringIO(sample_days)):
            self.assertEqual(download.get_num_days(),5)
            
        #Test Null input
        with patch("sys.stdin",new=StringIO("\n")):
            self.assertEqual(download.get_num_days(),7)
            
        #Test invalid input
        invalid_input="Just a random string"
        with patch("sys.stdin",new=StringIO(invalid_input)):
            self.assertEqual(download.get_num_days(),7)
    
