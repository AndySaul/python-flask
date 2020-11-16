from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "super secret key"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Items(Resource):
    @jwt_required()
    def get(self):
        return {"items": items}


class Item(Resource):
    @jwt_required()
    def get(self, name: str):
        item = self._item_with_name(name)
        return {"item": item}, 200 if item else 404

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
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": f"'{name}' item deleted"}

    @jwt_required()
    def put(self, name: str):
        params = self._parse_params()
        item = self._item_with_name(name)
        if item is None:
            item = self._store_item(name, params["price"])
        else:
            item.update(params)
        return item

    def _item_with_name(self, name: str):
        return next(filter(lambda x: x["name"] == name, items), None)

    def _parse_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument("price", type=float, required=True, help="Price cannot be blank")
        return parser.parse_args()

    def _store_item(self, name: str, price: float):
        item = {"name": name, "price": price}
        items.append(item)
        return item


api.add_resource(Items, "/items")
api.add_resource(Item, "/item/<string:name>")

app.run(port=5000, debug=True)
