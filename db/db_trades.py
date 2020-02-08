from db.db_setting import DB_connection
from psycopg2 import errors

class DB_trades():
    def __init__(self):
        # Create connection and cursor.
        self.conn = DB_connection().db_set()
        self.cursor = self.conn.cursor()

    def close_conn(self):
        #Close connection and cursor
        self.cursor.close()
        self.conn.close()

    def create_table_trades(self):
        """
        currency_in,currency_out = crypto currency/fiat currency or reverse
        :return:
        """
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS trades (id SERIAL PRIMARY KEY,trade_date TIMESTAMP,curr_in VARCHAR (3) NOT NULL,curr_out VARCHAR (3) NOT NULL,'
            'amount DECIMAL,exchange_id INT references crypto_exchanges(ID))')
        self.conn.commit()

    

DB_trades().create_table_trades()