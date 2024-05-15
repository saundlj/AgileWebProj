from unittest import TestCase
from app import create_app, db
from app.config import TestConfig
from app.controllers import NewUserError, create_user

# TO RUN
# python -m unittest test/unit.py

# test hashing password

# errors for login - invalid characters in email, email doesn't exist, wrong password
# errors for signup - invalid characters, username taken, email taken

# user create invalid job listing
# user create valid job listing

# user applies for job 
# user cannot apply for own job   

# test should not include real user data or data that changes over time
# dont want test to rely on external environment


class BasicUnitTests(TestCase):

    # init db with test data
    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()

    # clear db and remove all sessions
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # test passes when throws an error
    # raise error at multiple points
    # could fail at wrong point

    def test_new_user_username_taken(self):
        with self.assertRaisesRegex(NewUserError, "blah blah"): # provide exact error message and raise right exception 
            create_user("arguments") # relies on database being here and models set up 
        
