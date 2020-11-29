from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Items(Resource):
    @jwt_required()
    def get(self):
        return ItemModel.all_items()


class Item(Resource):
    @jwt_required()
    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message": f"An item named '{name}' already exists"}, 400

        params = self._parse_params()
        item = ItemModel(name, params["price"])
        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name: str):
        item = ItemModel(name, None)
        item.remove()
        return {"message": f"'{name}' item deleted"}

    @jwt_required()
    def put(self, name: str):
        params = self._parse_params()
        item = ItemModel(name, params['price'])

        if not ItemModel.find_by_name(name):
            try:
                item.insert()
            except:
                return {"message": "An error occurred inserting this item"}, 500
        else:
            try:
                item.update()
            except:
                return {"message": "An error occurred updating this item"}, 500
        return item.json()

    def _parse_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument("price", type=float, required=True, help="Price cannot be blank")
        return parser.parse_args()
