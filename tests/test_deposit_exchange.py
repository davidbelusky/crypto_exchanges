import unittest
from main_server import app
from flask import json
from models.others import *
from db.db_setting import DB_connection

class Test_Deposit_exchange(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.testing = True
        self.app = app.test_client()

        # Set and create testing table
        self.conn = DB_connection().db_set()
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS test_crypto_exchanges (id SERIAL PRIMARY KEY,name VARCHAR UNIQUE NOT NULL,curr VARCHAR (3) NOT NULL,amount DECIMAL)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS test_deposits (ID SERIAL PRIMARY KEY,deposit_date TIMESTAMP,exchange_id INT references test_crypto_exchanges(ID),curr VARCHAR NOT NULL,amount DECIMAL)')
        self.cursor.execute("INSERT INTO test_crypto_exchanges VALUES (DEFAULT, %s, %s, %s)",('Test_name', 'EUR', 0))
        self.conn.commit()


    # Type of input must be in JSON format
    def test_json_input(self):
        response = self.app.post('/exchanges/1/',data='text',content_type='application/json')
        self.assertEqual(response.status_code,400)

    # Amount must be float type
    def test_amount_type(self):
        response = self.app.post('/exchanges/1/', data=json.dumps({'currency': 'EUR', 'amount': 'abc'}),content_type='application/json')
        self.assertEqual(response.status_code,400)

    # Currency exist check
    def test_currency_exist_incorrect(self):
        response = self.app.post('/exchanges/1/', data=json.dumps({'currency': 'ABC', 'amount': 1}),content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # Currency exist check
    def test_currency_exist_correct(self):
        response = self.app.post('/exchanges/1/', data=json.dumps({'currency': 'EUR', 'amount': 1}),content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        #Drop created table for testing and close postgresql connections
        self.cursor.execute('DROP TABLE test_deposits')
        self.cursor.execute('DROP TABLE test_crypto_exchanges')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
