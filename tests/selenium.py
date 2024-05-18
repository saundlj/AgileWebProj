import multiprocessing
import time

from selenium import webdriver


from unittest import TestCase
from app import create_app, db
from app.config import TestConfig
from threading import Thread
from app.controllers import NewUserError, new_user
from app.models import User
from test_data import add_test_users_to_db

localHost = "http://localhost:5000/"

# python -m unittest tests/selenium.py

class SeliniumTestCase(TestCase):

    def setUp(self):
        # self.testApp = create_app(TestConfig)
        # self.app_context = self.testApp.app_context()
        # self.app_context.push()
        # db.drop_all()
        # db.create_all()
        # add_test_users_to_db()

        # # server responds to text
        # # self.server_process = multiprocessing.Process(target=self.testApp.run)
        # # self.server_process.start()
        # self.server_thread = Thread(target=self.testApp.run, kwargs=localHost)
        # self.server_thread.start()


        # self.driver = webdriver.Chrome()
        # self.driver.get(localHost)

        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        add_test_users_to_db()

        # Start the Flask server in a separate thread
        self.server_thread = Thread(target=self.testApp.run, kwargs={'port': 5000})
        self.server_thread.daemon = True  # Ensures the thread will be killed once the main program exits
        self.server_thread.start()

        # Wait a bit to ensure the server has started
        time.sleep(2)

        # Set up Selenium WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get(localHost)



    def tearDown(self):
        # db.session.remove()
        # db.drop_all()
        # self.app_context.pop()

        # # self.server_process.terminate()
        # # self.driver.close()

        # self.driver.quit()
        # # Stop the Flask server
        # self.server_thread.join()
        self.driver.quit()

        # Flask doesn't provide a built-in way to stop the server when running in a thread
        # Thus, we manually stop it if necessary
        if self.server_thread.is_alive():
            self.server_thread._stop()

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_group_page(self):
        time.sleep(10)
        self.assertTrue(True)
    