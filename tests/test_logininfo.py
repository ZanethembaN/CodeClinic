
import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

from system_configuration.command_line.login.logininfo import *

class TestOtpGeneretion(unittest.TestCase):

    def test_get_otp_length(self):

        code = get_otp()
        self.assertEqual(len(code), 6)

    def test_get_otp_type(self):
        code = get_otp()
        self.assertEqual(type(code), str)
        
    def test_get_otp_range(self):
        code = get_otp()
        for j in code:
            self.assertEqual(int(j) > 9, False)
            self.assertEqual(int(j) < 0, False)

class TestVerifyOTP(unittest.TestCase):

    def test_verify_otp_correct(self):
        self.assertTrue(verify_otp('123456', '123456'))

    def test_verify_otp_incorrect(self):
        self.assertFalse(verify_otp('654321', '123456'))

class TestLoginFunction(unittest.TestCase):

    @patch('builtins.input', side_effect=['test@student.wethinkcode.co.za'])
    @patch('system_configuration.command_line.login.logininfo.maskpass.askpass', return_value='password')
    def test_login_successful(self, mock_askpass, mock_input):

        data = [{"Email": "test@student.wethinkcode.co.za", "Password": "password"}]
        expected_output = "test@student.wethinkcode.co.za"
        
        with StringIO() as output,redirect_stdout(output) :
            result = login(data)
            out = output.getvalue()

        self.assertEqual(result, expected_output)
        self.assertIn("log in successful!!", out)



if __name__ == '__main__':
    unittest.main()


