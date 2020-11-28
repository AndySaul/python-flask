from resources.database import Database


class User:
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
        with Database() as db:
            result = db.execute(query, (param,))
            row = result.fetchone()
            if row:
                return cls(*row)
        return None

    @classmethod
    def create_table(cls):
        with Database() as db:
            db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)")
