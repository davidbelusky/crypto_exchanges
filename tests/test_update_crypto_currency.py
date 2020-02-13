import unittest
from main_server import app
from flask import json
from models.others import *
from db.db_setting import DB_connection

class Test_Add_crypto_exchange(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.testing = True
        self.app = app.test_client()

        # Set and create testing table
        self.conn = DB_connection().db_set()
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS test_crypto_exchanges (id SERIAL PRIMARY KEY,name VARCHAR UNIQUE NOT NULL,curr VARCHAR (3) NOT NULL,amount DECIMAL)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS test_crypto_currencies (id SERIAL PRIMARY KEY,name VARCHAR NOT NULL,curr VARCHAR (3) NOT NULL,favourite BOOLEAN NOT NULL,amount DECIMAL,exchange_id INT references test_crypto_exchanges(ID))')
        self.cursor.execute("INSERT INTO test_crypto_exchanges VALUES (DEFAULT, %s, %s, %s)", ('Test_name', 'EUR', 0))
        self.conn.commit()

    # Incorrect name input
    def test_check_crypto_name_exist_incorrect(self):
        response = self.app.put('/exchanges/1/currencie/', data=json.dumps({'name': 'abcde'}),content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # Correct name input
    def test_check_crypto_name_exist_correct(self):
        response = self.app.put('/exchanges/1/currencie/', data=json.dumps({'name': 'Bitcoin'}),content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # Incorrect currency input
    def test_check_crypto_currency_exist_incorrect(self):
        response = self.app.put('/exchanges/1/currencie/', data=json.dumps({'currency': 'abcde'}),content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # Correct currency input
    def test_check_crypto_currency_exist_correct(self):
        response = self.app.put('/exchanges/1/currencie/', data=json.dumps({'currency': 'BTC'}),content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # Name,currency,favourite input
    def test_json_response(self):
        response = self.app.put('/exchanges/1/currencie/', data=json.dumps({'name':'Bitcoin','currency': 'BTC','favourite':True}),content_type='application/json')
        json_keys_response = list(response.json[0].keys())
        json_keys_response.sort()
        key_list = ['amount', 'curr', 'exchange_id', 'favourite', 'id', 'name']
        key_list.sort()
        self.assertListEqual(json_keys_response, key_list)

    def tearDown(self):
        # Drop created table for testing and close postgresql connections
        self.cursor.execute('DROP TABLE test_crypto_currencies')
        self.cursor.execute('DROP TABLE test_crypto_exchanges')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
