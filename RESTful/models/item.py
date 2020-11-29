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
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
