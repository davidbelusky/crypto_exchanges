import unittest
from main_server import app
from flask import json,request
from models.others import *
import requests

class Test_Deposit_exchange(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.testing = True
        self.app = app.test_client()
#        response = self.app.post('/exchanges/',data=json.dumps({'name': 1, 'currency': 'eur'}),content_type='application/json')

    #Raise error 400 if was inputted string format not json

    # Type of input must be in JSON format
    def test_json_input(self):
        response = self.app.post('/exchanges/66',data='text',content_type='application/json')
        self.assertEqual(response.status_code,400)

    # Amount must be float type
    def test_amount_type(self):
        response = self.app.post('/exchanges/66', data=json.dumps({'currency': 'EUR', 'amount': 'abc'}),content_type='application/json')
        self.assertEqual(response.status_code,400)

    # Currency exist check
    def test_currency_exist_incorrect(self):
        response = self.app.post('/exchanges/66', data=json.dumps({'currency': 'ABC', 'amount': 1}),content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # Currency exist check
    def test_currency_exist_correct(self):
        response = self.app.post('/exchanges/66', data=json.dumps({'currency': 'EUR', 'amount': 1}),content_type='application/json')
        self.assertEqual(response.status_code, 200)








if __name__ == '__main__':
    unittest.main()
