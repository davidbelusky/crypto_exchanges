import unittest
from main_server import app

class TestExample(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.testing = True
        self.app = app.test_client()
        pass

    def test_equal_numbers_ok(self):
        self.assertEqual(2, 2)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        #self.assertEqual(response.data, b"<h1>My first REST API</h1>")

if __name__ == '__main__':
    unittest.main()
