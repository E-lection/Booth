from flask import Flask
import application
import unittest
import models as db
import create_user

TEST_USERNAME = 'booth_test'
TEST_PASSWORD = 'test_secret'
TEST_STATION_ID = 1
BAD_LOGIN = 'bad'

class BoothTestCase(unittest.TestCase):

    def setUp(self):
        application.application.config['TESTING'] = True
        self.application = application.application.test_client()
        create_user.create_user(TEST_USERNAME, TEST_PASSWORD, TEST_STATION_ID)

    def tearDown(self):
        db.deleteUser('booth_test')

    # Login booth helper function
    def login(self):
        self.application.post('/login', data=dict(
            username=TEST_USERNAME,
            password=TEST_PASSWORD
        ))

    def test_home_status_code_not_logged_in(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.application.get('/')

        # assert the status code of the response for redirection
        self.assertEqual(result.status_code, 302)

    def test_home_status_code_logged_in(self):
        self.login()
        result = self.application.get('/')

        # assert the status code of the response for redirection
        self.assertEqual(result.status_code, 200)

    def test_enter_pin_field_logged_in(self):
        self.login()
        result = self.application.get('/')

        assert b'Type in your 6 digit PIN and press Enter' in result.data

if __name__ == '__main__':
    unittest.main()
