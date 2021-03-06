from db.db_setting import DB_connection
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from models.others import DecimalEncoder

class DB_crypto_currencies():
    def __init__(self):
        #Create connection and cursor.
        self.conn = DB_connection().db_set()
        self.cursor = self.conn.cursor()
        #self.create_tables_exchanges()

    def close_conn(self):
        #Close connection and cursor
        self.cursor.close()
        self.conn.close()

    def create_table_crypto_currencies(self):
        """
        Name is unique only for exchange id
        :return:
        """
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS crypto_currencies (id SERIAL PRIMARY KEY,name VARCHAR NOT NULL,curr VARCHAR (3) NOT NULL,favourite BOOLEAN NOT NULL,amount DECIMAL,exchange_id INT references crypto_exchanges(ID))')
        self.conn.commit()

    def select_all_crypto_currencies(self):
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        self.cursor.execute("SELECT * FROM crypto_currencies")
        currencies = self.cursor.fetchall()
        #Convert returned decimals from DB to float
        for crypto_currency in currencies:
            crypto_currency['amount'] = DecimalEncoder().default(crypto_currency['amount'])
        return currencies

    def select_check_existed_currency(self,exchange_id,currency ):
        self.cursor.execute("SELECT curr,favourite FROM crypto_currencies WHERE exchange_id = '{}' AND curr = '{}'".format(exchange_id,currency))
        currency = self.cursor.fetchone()
        return currency

    def select_check_currencies_for_exchange_id(self,exchange_id):
        self.cursor.execute("SELECT curr FROM crypto_currencies WHERE exchange_id = '{}'".format(exchange_id))
        currencies = self.cursor.fetchall()
        currencies_lst = [currency[0] for currency in currencies]
        return currencies_lst

    def select_check_balance_amount(self,exchange_id,currency):
        self.cursor.execute("SELECT curr,amount FROM crypto_currencies WHERE exchange_id = '{}' AND curr = '{}'".format(exchange_id,currency))
        currency = self.cursor.fetchone()
        return currency

    def select_crypto_name(self,exchange_id,currency_in,currency_out):
        self.cursor.execute(
            "SELECT name FROM crypto_currencies WHERE exchange_id = '{}' AND (curr = '{}' OR curr = '{}') ".format(exchange_id,currency_in,currency_out))
        try:
            crypto_name = self.cursor.fetchone()[0]
        except TypeError:
            return {'message':'Crypto name was not founded for this exchange_id'}
        return crypto_name

    def insert_crypto_currency(self,json,testing):
        #If testing True create table for testing
        if testing: table = 'test_crypto_currencies'
        else: table = 'crypto_currencies'

        try:
            self.cursor.execute("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s, %s, %s)".format(table),
                                (json['name'], json['currency'], json['favourite'],0,json['exchange_id']))
        except errors.ForeignKeyViolation:
            return {'message':'exchange id: {} doesnt exist'.format(json['exchange_id'])},400

        self.conn.commit()
        self.close_conn()

    def delete_crypto_currency(self,json):
        self.cursor.execute("DELETE FROM crypto_currencies WHERE exchange_id = '{}' AND name = '{}'".format(json['exchange_id'],json['name']))
        self.conn.commit()
        self.close_conn()

    def update_crypto_currency(self,json):
        self.cursor.execute("UPDATE crypto_currencies SET favourite = '{}' WHERE exchange_id = '{}' AND name = '{}'".format(json['favourite'],json['exchange_id'],json['name']))
        self.conn.commit()
        self.close_conn()



