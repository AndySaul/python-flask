from resources.database import Database


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def create_table(cls):
        with Database() as db:
            db.execute("CREATE TABLE IF NOT EXISTS items (name text, price real)")

    @classmethod
    def find_by_name(cls, name: str):
        with Database() as db:
            query = "SELECT * FROM items WHERE name=?"
            result = db.execute(query, (name,))
            row = result.fetchone()
            if row:
                return cls(*row)

    def update(self):
        with Database() as db:
            db.execute("UPDATE items SET price=? WHERE name=?", (self.price, self.name))

    def insert(self):
        with Database() as db:
            query = "INSERT INTO items VALUES (?, ?)"
            db.execute(query, (self.name, self.price))
