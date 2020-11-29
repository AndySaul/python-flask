from resources.database import Database
from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def all_items(cls):
        with Database() as database:
            result = database.execute("SELECT * FROM items")
            items = []
            for row in result:
                item = cls(*row)
                items.append(item.json())
            return {"items": items}

    @classmethod
    def find_by_name(cls, name: str):
        with Database() as database:
            query = "SELECT * FROM items WHERE name=?"
            result = database.execute(query, (name,))
            row = result.fetchone()
            if row:
                return cls(*row)

    def update(self):
        with Database() as database:
            database.execute("UPDATE items SET price=? WHERE name=?", (self.price, self.name))

    def insert(self):
        with Database() as database:
            query = "INSERT INTO items VALUES (?, ?)"
            database.execute(query, (self.name, self.price))

    def remove(self):
        with Database() as database:
            database.execute("DELETE FROM items WHERE name=?", (self.name,))
