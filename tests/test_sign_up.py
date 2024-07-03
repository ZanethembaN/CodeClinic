import unittest
from unittest.mock import patch
from system_configuration.command_line.sign_up.sign_up import *
from system_configuration.command_line.authentication import creds_fetch

class TestValidateEmail(unittest.TestCase):

    def test_valid_email(self):
        valid_emails = [
            "example@student.wethinkcode.co.za",
            "username023@student.wethinkcode.co.za"
        ]
        for email in valid_emails:
            self.assertTrue(validate_email(email))

    def test_invalid_email(self):
        invalid_emails = [
            "example@invalid.com",
            "test.student.wethinkcode.co.za",
            "example@wethinkcode.co.za"
        ]
        for email in invalid_emails:
            self.assertFalse(validate_email(email))





if __name__ == '__main__':
    unittest.main()
