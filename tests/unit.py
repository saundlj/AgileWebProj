from unittest import TestCase
from app import create_app, db
from app.config import TestConfig
from app.controllers import NewUserError, new_user
from app.models import User
from test_data import add_test_users_to_db

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
        add_test_users_to_db()

    # clear db and remove all sessions
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # test passes when throws an error
    # raise error at multiple points
    # could fail at wrong point

    def test_new_username_invalid_char(self):
        with self.assertRaisesRegex(NewUserError, "Username contains at least one invalid character. Please remove and try again."): # provide exact error message and raise right exception 
            new_user(User(username='inval!d', first_name = "test", last_name = "test", email = "email@proj.com", password_hash = 'Admin2002'))

    def test_new_username_duplicate(self):
        with self.assertRaisesRegex(NewUserError, "Username already exists. Please try another."): # provide exact error message and raise right exception 
            new_user(User(username='testing', first_name = "test", last_name = "test", email = "email@proj.com", password_hash = 'Admin2002'))

    def test_new_first_name_invalid_char(self):
        with self.assertRaisesRegex(NewUserError, "First Name contains at least one invalid character. Please remove and try again."): # provide exact error message and raise right exception 
            new_user(User(username='testing2', first_name = "test_", last_name = "test", email = "email@proj.com", password_hash = 'Admin2002'))

    def test_new_last_name_invalid_char(self):
        with self.assertRaisesRegex(NewUserError, "Last Name contains at least one invalid character. Please remove and try again."): # provide exact error message and raise right exception 
            new_user(User(username='testing2', first_name = "test", last_name = "test_", email = "email@proj.com", password_hash = 'Admin2002'))

    def test_new_email_invalid_char(self):
        with self.assertRaisesRegex(NewUserError, "Email contains at least one invalid character. Please remove and try again."): # provide exact error message and raise right exception 
            new_user(User(username='testing2', first_name = "test", last_name = "test", email = "emai#@proj.com", password_hash = 'Admin2002'))  

    def test_new_email_duplicate(self):
        with self.assertRaisesRegex(NewUserError, "Email already registered. Please Login instead."): # provide exact error message and raise right exception 
            new_user(User(username='testing2', first_name = "test", last_name = "test", email = "email@proj.com", password_hash = 'Admin2002'))  

    # def test_password_hashing(self):
    #     user = User.query.get(1)
    #     s.set_password("bubbles")
    #     self.assertTrue(s.check_password("bubbles"))
    #     self.assertFalse(s.check_password("rabbles"))
