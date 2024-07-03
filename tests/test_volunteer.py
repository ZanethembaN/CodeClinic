import sys,os
print(os.getcwd())
import unittest
from unittest.mock import patch
from volunteer_slot import volunteer 



class volunteerTestCase(unittest.TestCase):
    def test_validate_time_input(self):
        #Test no colon
        self.assertEqual( [False,False],volunteer.validate_time_input("aabb"),"Expected ':' in input")
        #Test Hours invalid input but minutes valid
        self.assertEqual([False,True],volunteer.validate_time_input("aa:00"),"Response doesn't validate hours ")
        #Test Hours valid but minutes invalid
        self.assertEqual([True,False],volunteer.validate_time_input("14:aa"),"Response doesn't validate minutes")
        #Test Hours out of range but minutes in range
        self.assertEqual([False,True],volunteer.validate_time_input("31:00"),"Hours range not validated properly")
        #Test Hours in range but minutes out of range
        self.assertEqual([True,False],volunteer.validate_time_input("20:61"),"Minutes range not validated properly")
        #Test Valid Hours and minutes
        self.assertEqual([True,True],volunteer.validate_time_input("15:30"),"Valid input rejected")
        #Test Invalid Length
        self.assertEqual([False,False],volunteer.validate_time_input("15:300"),"Invalid length for hours or minutes")
        
    def test_choose_slot(self):
        pass


    def test_slot_day_valid(self):
        pass
    
    
    def test_confirm_slot(self):
        pass