from unittest import TestCase
from app.controllers import create_user

# TO RUN
# python -m unittest test/unit.py

# test hashing password
# database working?
# correct error for login
# correct error for signup
# new user signup valid
# existing user login

# user create invalid job listing
# user create valid job listing

# user applies for job 
# user cannot apply for own job   

# test should not include real user data or data that changes over time
# dont want test to rely on external environment


class BasicUnitTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # test passes when throws an error
    # raise error at multiple points
    # could fail at wrong point

    def test_create_user_existing_username(self):
        with self.assertRaisesRegex(NewUserError, "blah blah"): # provide exact error message and raise right exception 
            create_user("arguments") # relies on database being here and models set up 
        
