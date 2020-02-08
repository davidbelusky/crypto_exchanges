from db_setting import DB_connection

class DB_test():
    def __init__(self):
        self.conn = DB_connection().db_set()
        self.cursor = self.conn.cursor()

    def close_conn(self):
        self.cursor.close()
        self.conn.close()

    def create_table(self):

    def select_all(self):
        self.cursor.execute("SELECT * FROM d_movie")
        result = self.cursor.fetchall()
        print(result)
        self.close_conn()


DB_test().select_all()