import sqlite3


class Database:
    def __init__(self, name='data.db'):
        self._name = name
        self._connection = None
        self._cursor = None

    def __enter__(self):
        self._connection = sqlite3.connect(self._name)
        self._cursor = self._connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.commit()
        self._connection.close()

    def execute(self, *args):
        return self._cursor.execute(*args)
