from flask import Flask
import application
import unittest
import models as db
import create_user

class BoothTestCase(unittest.TestCase):

    def setUp(self):
        application.application.config['TESTING'] = True
        self.application = application.application.test_client()
        create_user.create_user('booth_test', 'test_secret', 1)

    def tearDown(self):
        db.deleteUser('booth_test')

    # Login booth helper function
    def login(self):
        self.application.post('/login', data=dict(
            username='booth_test',
            password='test_secret'
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

if __name__ == '__main__':
    unittest.main()
