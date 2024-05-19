from unittest import TestCase
from app import create_app, db
from app.config import TestConfig
from app.controllers import ApplicationFormError, JobPostError, LoginUserError, NewUserError, UserAccountFormError, new_user, log_in, new_job_post, new_bio, new_application
from app.models import Post, User, Application
from test_data import *

# TO RUN
# python -m unittest test/unit.py

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
            new_user(User(username='tesemail2', first_name = "tester", last_name = "tested", email = "admin@proj.com", password_hash = 'Admin2002'))  

    def test_password_hashing(self):   
        db.session.add(User(username='passwordcheck', first_name = "tester", last_name = "tested", email = "password@proj.com", password_hash = 'Random123#'))
        user = User.query.get(3)
        user.set_password(user.password_hash) # hash password
        self.assertTrue(user.check_password("Random123#"))
        self.assertFalse(user.check_password("RandomPassword#"))

    def test_login_email_invalid(self):
        with self.assertRaisesRegex(LoginUserError, "Email contains at least one invalid character. Please remove and try again."):
            log_in("p#fr%@gmail.com", "password")

    def test_login_email_not_registed(self):
        with self.assertRaisesRegex(LoginUserError, "Email entered is not registered. Try creating an account!"):
            log_in("randomemail@gmail.com", "password")

    def test_login_wrong_password(self):
        with self.assertRaisesRegex(LoginUserError, "Password entered does not match registered email. Please try again."):
            log_in("admin@proj.com", "password")

    def test_user_post_desciption_invalid_char(self):
        with self.assertRaisesRegex(JobPostError, "Description contains at least one invalid character. Please remove and try again."):
            new_job_post(Post(title = 'Test Post',
             location = 'Somewhere Important',
             job_type = 'Life',
             description = 'This data is stored in the database with lots of ;; S inval%id c~~arcters++',
             user_id = 2))

    def test_user_post_same_title(self):
        with self.assertRaisesRegex(JobPostError, "You already have a Post with the same title."):
            new_job_post(Post(title = 'Test Post',
             location = 'Somewhere Important',
             job_type = 'Life',
             description = 'This data is stored in the database',
             user_id = 1))
            
    def test_userbio_historic_startdate(self):
        with self.assertRaisesRegex(UserAccountFormError,"Earliest start date cannot be before todays date!"):
            new_bio(Account(earliest_start_date=datetime(2000, 1, 1)))

    def test_user_apply_own_post(self):
        with self.assertRaisesRegex(ApplicationFormError, "Cannot apply for your own job post!"):
            app = Application(user_id = 1, post_id = 1, cover_letter = "You should not be allowed to apply to your own job.")
            post = Post.query.filter_by(id=1).first()
            new_application(app, post)