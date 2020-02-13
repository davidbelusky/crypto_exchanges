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

    # Type of input must be in JSON format
    def test_json_input(self):
        response = self.app.post('/exchanges/',data='text',content_type='application/json')
        self.assertEqual(response.status_code,400)

    # Name cannot obtain any special character
    def test_validate_name_special_characters(self):
        response = self.app.post('/exchanges/', data=json.dumps({'name': 'First_exchange2@@', 'currency': 'eur'}),content_type='application/json')
        self.assertEqual(response.status_code,400)

    # Name can obtain numbers and underscore
    def test_validated_name(self):
        response = self.app.post('/exchanges/', data=json.dumps({'name': 'First_exchange1', 'currency': 'eur'}),content_type='application/json')
        print(response.json)
        self.assertEqual(response.status_code, 200)

    # Validating length of inputted currency
    def test_validate_length_currency(self):
        response = self.app.post('/exchanges/', data=json.dumps({'name': 'First_exchange1', 'currency': 'sf'}),content_type='application/json')
        self.assertEqual(response.status_code, 400)
    # Check if currency exist
    def test_validate_incorrect_currency(self):
        response = self.app.post('/exchanges/', data=json.dumps({'name': 'First_exchange1', 'currency': 'AAA'}),content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # Check if currency exist
    def test_validate_correct_currency(self):
        response = self.app.post('/exchanges/', data=json.dumps({'name': 'Second_exchange2', 'currency': 'USD'}),content_type='application/json')
        self.assertEqual(response.status_code, 200)




if __name__ == '__main__':
    unittest.main()
