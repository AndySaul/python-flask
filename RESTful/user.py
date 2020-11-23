import sqlite3
from flask_restful import Resource, reqparse


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


class User:
    def __init__(self, _id, username: str, password: str):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        with Database() as db:
            query = "SELECT * FROM users WHERE username=?"
            result = db.execute(query, (username,))
            row = result.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def find_by_id(cls, _id):
        with Database() as db:
            query = "SELECT * FROM users WHERE id=?"
            result = db.execute(query, (_id,))
            row = result.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def create_table(cls):
        with Database() as db:
            create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
            db.execute(create_table)


class RegisterUser(Resource):

    def post(self):
        User.create_table()

        params = self._parse_params()
        if User.find_by_username(params['username']):
            return {'message': "User already registered"}, 400

        with Database() as db:
            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            args = (params['username'], params['password'])
            db.execute(query, args)
        return {'message': "User created successfully"}, 201

    @staticmethod
    def _parse_params():
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        return parser.parse_args()
