from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from resources.database import Database
from models.item import ItemModel


class Items(Resource):
    @jwt_required()
    def get(self):
        with Database() as db:
            result = db.execute("SELECT * FROM items")
            items = []
            for row in result:
                items.append({"name": row[0], "price": row[1]})
            return {"items": items}


class Item(Resource):
    @jwt_required()
    def get(self, name: str):
        item = ItemModel.with_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name: str):
        item = ItemModel.with_name(name)
        if item:
            return {"message": f"An item named '{name}' already exists"}, 400

        params = self._parse_params()
        item = ItemModel.store(name, params["price"])
        return item, 201

    @jwt_required()
    def delete(self, name: str):
        with Database() as db:
            db.execute("DELETE FROM items WHERE name=?", (name,))
        return {"message": f"'{name}' item deleted"}

    @jwt_required()
    def put(self, name: str):
        params = self._parse_params()
        item = ItemModel.with_name(name)
        if item is None:
            try:
                item = ItemModel.store(name, params['price'])
            except:
                return {"message": "An error occurred inserting this item"}, 500
        else:
            try:
                item = ItemModel.update(name, params['price'])
            except:
                return {"message": "An error occurred updating this item"}, 500
        return item

    def _parse_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument("price", type=float, required=True, help="Price cannot be blank")
        return parser.parse_args()
