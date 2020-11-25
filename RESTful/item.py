from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from database import Database


class Items(Resource):
    @jwt_required()
    def get(self):
        with Database() as db:
            result = db.execute("SELECT * FROM items")
            items = []
            for row in result:
                items.append({"name": row[0], "price": row[1]})
            return {"items": items}

    @classmethod
    def create_table(cls):
        with Database() as db:
            db.execute("CREATE TABLE IF NOT EXISTS items (name text, price real)")


class Item(Resource):
    @jwt_required()
    def get(self, name: str):
        item = self._item_with_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name: str):
        item = self._item_with_name(name)
        if item:
            return {"message": f"An item named '{name}' already exists"}, 400

        params = self._parse_params()
        item = self._store_item(name, params["price"])
        return item, 201

    @jwt_required()
    def delete(self, name: str):
        with Database() as db:
            db.execute("DELETE FROM items WHERE name=?", (name,))
        return {"message": f"'{name}' item deleted"}

    @jwt_required()
    def put(self, name: str):
        params = self._parse_params()
        item = self._item_with_name(name)
        if item is None:
            try:
                item = self._store_item(name, params['price'])
            except:
                return {"message": "An error occurred inserting this item"}, 500
        else:
            try:
                item = self._update(name, params['price'])
            except:
                return {"message": "An error occurred updating this item"}, 500
        return item

    @classmethod
    def _item_with_name(cls, name: str):
        with Database() as db:
            query = "SELECT * FROM items WHERE name=?"
            result = db.execute(query, (name,))
            row = result.fetchone()
            if row:
                return {'item': {'name': row[0], 'price': row[1]}}

    def _parse_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument("price", type=float, required=True, help="Price cannot be blank")
        return parser.parse_args()

    def _store_item(self, name: str, price: float):
        with Database() as db:
            query = "INSERT INTO items VALUES (?, ?)"
            db.execute(query, (name, price))
            return {"name": name, "price": price}

    @classmethod
    def _update(cls, name, price):
        with Database() as db:
            db.execute("UPDATE items SET price=? WHERE name=?", (price, name))
        return {"name": name, "price": price}
