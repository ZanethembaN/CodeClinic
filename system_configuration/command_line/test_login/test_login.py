import unittest
from unittest.mock import patch
from io import StringIO
from greetings.hello import say_hello
from leaving.goodbye import say_goodbye
from login.logininfo import logindata
import sys


class TestTryScript(unittest.TestCase):

    def test_hello(self):
        args = {'hello': True, '<name>': 'John'}
        result = say_hello(args['<name>'])
        expected_output = "Hello, John"
        self.assertEqual(result, expected_output)

    def test_goodbye(self):
        args = {'goodbye': True, '<name>': 'Alice'}
        result = say_goodbye(args['<name>'])
        expected_output = "Goodbye, Alice"
        self.assertEqual(result, expected_output)

    def test_logindata(self):
        with patch('builtins.input', side_effect=['test@example.com']), \
             patch('getpass.getpass', return_value='test_password'):
            result = logindata()
        expected_output = "Log In:\nLogin Successful!\n"
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
