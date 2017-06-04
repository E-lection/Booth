import application
import unittest

class BoothTestCase(unittest.TestCase):

    def setUp(self):
        application.application.config['TESTING'] = True
        self.application = application.application.test_client()

    def tearDown(self):
        pass

    def test_home_status_code(self):
        result = self.application.get('/')
        self.assertEqual(result.status_code, 200)
