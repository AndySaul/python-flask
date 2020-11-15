from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Items(Resource):
    def get(self):
        return {"items": items}


class Item(Resource):
    def get(self, name):
        item = self._item_with_name(name)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        item = self._item_with_name(name)
        if item:
            return {'message': f"An item named '{name}' already exists"}, 400
        param = request.get_json()
        item = {"name": name, "price": param["price"]}
        items.append(item)
        return item, 201

    def _item_with_name(self, name):
        return next(filter(lambda x: x["name"] == name, items), None)


api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=5000, debug=True)
