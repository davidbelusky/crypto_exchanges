import unittest
from main_server import app
from flask import json,request
from models.others import *
import requests

class Test_Add_crypto_exchange(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.testing = True
        self.app = app.test_client()
#        response = self.app.post('/exchanges/',data=json.dumps({'name': 1, 'currency': 'eur'}),content_type='application/json')

    #Raise error 400 if was inputted string format not json

    # Incorrect name input
    def test_check_crypto_name_exist_incorrect(self):
        response = self.app.put('/exchanges/66/currencie/', data=json.dumps({'name': 'abcde'}),content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # Correct name input
    def test_check_crypto_name_exist_correct(self):
        response = self.app.put('/exchanges/66/currencie/', data=json.dumps({'name': 'Bitcoin'}),content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # Incorrect currency input
    def test_check_crypto_currency_exist_incorrect(self):
        response = self.app.put('/exchanges/66/currencie/', data=json.dumps({'currency': 'abcde'}),content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # Correct currency input
    def test_check_crypto_currency_exist_correct(self):
        response = self.app.put('/exchanges/66/currencie/', data=json.dumps({'currency': 'BTC'}),content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # Name,currency,favourite input
    def test_json_response(self):
        response = self.app.put('/exchanges/66/currencie/', data=json.dumps({'name':'Bitcoin','currency': 'BTC','favourite':True}),content_type='application/json')
        json_keys_response = list(response.json[0].keys())
        json_keys_response.sort()
        key_list = ['amount', 'curr', 'exchange_id', 'favourite', 'id', 'name']
        key_list.sort()
        self.assertListEqual(json_keys_response, key_list)






if __name__ == '__main__':
    unittest.main()
