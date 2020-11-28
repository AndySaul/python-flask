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
    def with_name(cls, name: str):
        with Database() as db:
            query = "SELECT * FROM items WHERE name=?"
            result = db.execute(query, (name,))
            row = result.fetchone()
            if row:
                return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def update(cls, name, price):
        with Database() as db:
            db.execute("UPDATE items SET price=? WHERE name=?", (price, name))
        return {"name": name, "price": price}

    @classmethod
    def store(self, name: str, price: float):
        with Database() as db:
            query = "INSERT INTO items VALUES (?, ?)"
            db.execute(query, (name, price))
            return {"name": name, "price": price}
