from db.db_setting import DB_connection
from psycopg2 import errors
from models.exchange_model import *

class DB_exchanges():
    def __init__(self):
        #Create connection and cursor.
        self.conn = DB_connection().db_set()
        self.cursor = self.conn.cursor()
        #self.create_tables_exchanges()

    def close_conn(self):
        #Close connection and cursor
        self.cursor.close()
        self.conn.close()

    def create_tables_exchanges(self):
        """
        Try to create tables for add exchanges and deposit exchange
        :return:
        """

        self.cursor.execute('CREATE TABLE IF NOT EXISTS crypto_exchanges (id SERIAL PRIMARY KEY,name VARCHAR UNIQUE NOT NULL,curr VARCHAR (3) NOT NULL,amount DECIMAL)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS deposits (ID SERIAL PRIMARY KEY,deposit_date TIMESTAMP,exchange_id INT references crypto_exchanges(ID),curr VARCHAR NOT NULL,amount DECIMAL)')
        self.conn.commit()

    def insert_exchange(self,json,testing):
        """
        Insert new unique crypto exchange.
        :param json: json with unique name and currency
        :return: IF success inserted json, ELSE message
        """
        if testing: table = 'test_crypto_exchanges'
        else: table = 'crypto_exchanges'

        try:
            self.cursor.execute("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s) RETURNING *".format(table),
                                (json['name'],json['currency'],0))
        except errors.UniqueViolation:
            #If name already exist in table return message
            return {'message': 'Name is already in DB'},400
        self.conn.commit()
        id,name,currency,amount = self.cursor.fetchone()
        self.close_conn()
        json_return = {'id':id,'name':name,'currency':currency}

        return json_return

    def insert_deposit_exchange(self,json,testing):
        if testing: exchange_table,deposit_table = ['test_crypto_exchanges','test_deposits']
        else: exchange_table,deposit_table = ['crypto_exchanges','deposits']

        exchange_currency = self.select_check_exchange(json['exchange_id'],exchange_table)
        if exchange_currency == None:
            return {'message':'Exchange id doesnt exist'},400
        #Get currency and actual amount of exchange id
        exchange_currency,actual_exchange_amount = exchange_currency

        converted_amount = Add_exchange_model().deposit_convert_currency(json['currency'],exchange_currency,json['amount'])
        total_amount = float(converted_amount + float(actual_exchange_amount))
        #If testing = True set table for testing

        self.cursor.execute("INSERT INTO {} VALUES (DEFAULT, NOW(), %s, %s, %s)".format(deposit_table),
                               (json['exchange_id'],json['currency'],json['amount']))

        self.cursor.execute("UPDATE {} SET amount = {} WHERE  id = {}".format(exchange_table,total_amount,json['exchange_id']))

        self.conn.commit()
        self.close_conn()
        return 'success'

    def select_check_exchange(self,exchange_id,table = 'crypto_exchanges'):
        self.cursor.execute("SELECT curr,amount FROM {} WHERE id = '{}'".format(table,exchange_id))
        currency = self.cursor.fetchone()
        return currency

