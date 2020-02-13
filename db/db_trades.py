from db.db_setting import DB_connection
from psycopg2.extras import RealDictCursor
from models.others import DecimalEncoder
from models.others import Trade_history_sql_generate


class DB_trades():
    def __init__(self):
        # Create connection and cursor.
        self.conn = DB_connection().db_set()
        self.cursor = self.conn.cursor()
        #self.create_table_trades()

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
            'CREATE TABLE IF NOT EXISTS trades (id SERIAL PRIMARY KEY,trade_date TIMESTAMP,name VARCHAR,curr_in VARCHAR (3) NOT NULL,curr_out VARCHAR (3) NOT NULL,'
            'amount DECIMAL,exchange_id INT references crypto_exchanges(ID))')
        self.conn.commit()

    def update_amount_trade_exchange(self, exchange_id, trade_amount,operator):
        """
        Update amount for exchange_id
        :param exchange_id:
        :param trade_amount: inputted amount for trade
        :param operator: plus + or substract -
        :return:
        """
        self.cursor.execute("UPDATE crypto_exchanges SET amount = amount {operator} {trade_amount} WHERE id = {exchange_id}".format(
            operator=operator,trade_amount=trade_amount,exchange_id=exchange_id))
        self.conn.commit()
        self.close_conn()

    def update_amount_trade_crypto(self,exchange_id,crypto_currency,trade_amount,operator):
        """
        Update amount for currency
        :param exchange_id: specific exchange id
        :param crypto_currency: inputted specific crypto currency
        :param trade_amount: inputted amount for trade
        :param operator: plus + or substract -
        :return:
        """
        self.cursor.execute("UPDATE crypto_currencies SET amount = amount {operator} {trade_amount} WHERE exchange_id = {exchange_id} AND curr = '{crypto_currency}'".format(
                operator=operator, trade_amount=trade_amount, exchange_id=exchange_id,crypto_currency=crypto_currency))
        self.conn.commit()
        self.close_conn()

    def select_actual_exchange_amount(self,currency_type,exchange_id,crypto_currency = None):
        if currency_type == False:
            self.cursor.execute("SELECT curr,amount FROM crypto_currencies WHERE exchange_id = '{}' AND curr = '{}'".format(exchange_id,crypto_currency))
        else:
            self.cursor.execute("SELECT curr,amount FROM crypto_exchanges WHERE id = '{}'".format(exchange_id))

        actual_amount = self.cursor.fetchone()
        dict_actual = {'actual_amount':float(actual_amount[1]),'currency':actual_amount[0]}
        return dict_actual

    def insert_trade_record(self,json):
        self.cursor.execute("INSERT INTO trades VALUES (DEFAULT, NOW(), %s, %s, %s, %s, %s)",
                            (json['crypto_name'],json['currency_in'], json['currency_out'], json['amount'],json['exchange_id']))

        self.conn.commit()
        self.close_conn()

    def select_trade_history(self,json):
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        #Generate SQL based on inputted parameters
        sql = Trade_history_sql_generate.generate_sql_history_filter(json)
        self.cursor.execute(sql)
        history_data = self.cursor.fetchall()
        # Convert decimals type to float. (json cannot obtain decimal type)
        for row in history_data:
            row['amount'] = DecimalEncoder().default(row['amount'])

        return history_data

    def select_all_trade_history(self):
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        self.cursor.execute("SELECT * FROM trades")
        all_history_data = self.cursor.fetchall()

        # Convert decimals type to float. (json cannot obtain decimal type)
        for row in all_history_data:
            row['amount'] = DecimalEncoder().default(row['amount'])
        return all_history_data




