import multiprocessing
import time

from selenium import webdriver


from unittest import TestCase
from app import create_app, db
from app.config import TestConfig
from app.controllers import NewUserError, new_user
from app.models import User
from test_data import add_test_users_to_db

localHost = "http://localhost:5000/"

# python -m unittest tests/selenium.py

class SeliniumTestCase(TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        # add_test_users_to_db()

        # server responds to text
        self.server_process = multiprocessing.Process(target=self.testApp.run)
        self.server_process.start()

        self.driver = webdriver.Chrome()
        self.driver.get(localHost)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()
        self.driver.close()

    def test_group_page(self):
        time.sleep(10)
        self.assertTrue(True)
    