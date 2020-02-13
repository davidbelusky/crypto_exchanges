import os, psycopg2
from dotenv import load_dotenv, find_dotenv

class DB_connection:

    def db_set(self):
        # Load env with DB settings
        load_dotenv(find_dotenv())
        # Create connection to DB
        connection = psycopg2.connect((os.getenv('DB')))
        return connection

