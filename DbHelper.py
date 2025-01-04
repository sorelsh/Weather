import sqlite3
import os

class DbWheather:

    def __init__(self,  **kwargs):
        self._filename = kwargs.get('filename', 'temp')
        self._table = kwargs.get('table', 'test')

        if not os.path.exists("Db"):
            os.makedirs("Db")

        with sqlite3.connect('Db/weatherDB.db') as conn:
            cursor = conn.cursor()
            if self._table != "test":
                create_statement = """CREATE TABLE IF NOT EXISTS {tableName} (
                                    country text NOT NULL, 
                                    city text NOT NULL,
                                    UNIQUE(country, city) ON CONFLICT REPLACE
                                    );"""
            cursor.execute(create_statement.format(tableName=self._table))
            conn.commit()

    def insert(self, row):
        with sqlite3.connect('Db/weatherDB.db') as conn:
            cursor = conn.cursor()
            cursor.execute('insert into {} (country, city) values (?, ?)'.format(self._table), (row['country'], row['city']))
            conn.commit()

    def retrieve(self, key):
        with sqlite3.connect('Db/weatherDB.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute('select city from {} where country = ?'.format(self._table), (key,))
            return res.fetchall()













