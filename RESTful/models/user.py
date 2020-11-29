from resources.database import Database
from db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username: str, password: str):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls._find_user("SELECT * FROM users WHERE username=?", username)

    @classmethod
    def find_by_id(cls, _id):
        return cls._find_user("SELECT * FROM users WHERE id=?", _id)

    @classmethod
    def _find_user(cls, query, param):
        with Database() as database:
            result = database.execute(query, (param,))
            row = result.fetchone()
            if row:
                return cls(*row)
        return None
