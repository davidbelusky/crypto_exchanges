import unittest
from main_server import app
from flask import json,request
from models.others import *
import requests

class Test_Create_trade(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.testing = True
        self.app = app.test_client()

    #Check if currencies are fiato to crypto or crypto to fiat
    def test_currencies_trade_incorrect(self):
        response = self.app.post('/exchanges/66/trades/', data=json.dumps({'amount': 0, 'currency_in': 'USD','currency_out':'EUR'}),content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # Check if currencies are fiato to crypto or crypto to fiat
    def test_currencies_trade_correct(self):
        response = self.app.post('/exchanges/66/trades/',data=json.dumps({'amount': 0, 'currency_in': 'USD', 'currency_out': 'BTC'}),content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # When balance amount < trade amount error
    def test_amounts_incorrect(self):
        response = self.app.post('/exchanges/66/trades/',data=json.dumps({'amount': 500, 'currency_in': 'USD', 'currency_out': 'BTC'}),content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # When balance amount >= trade amount OK
    def test_amounts_correct(self):
        response = self.app.post('/exchanges/66/trades/',data=json.dumps({'amount': 0, 'currency_in': 'USD', 'currency_out': 'BTC'}),content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()