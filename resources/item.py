# Copyright (c) Andy Saul 2020

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_claims, get_jwt_identity

from models.item import ItemModel


class Items(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {'items': [item['name'] for item in items], 'message': 'More data available if you log in'}, 200


class Item(Resource):

    @jwt_required
    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required
    def post(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message": "Item already exists"}, 400

        params = parse_params()
        item = ItemModel(name, **params)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201

    @jwt_required
    def delete(self, name: str):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}

    @jwt_required
    def put(self, name: str):
        params = parse_params()
        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, **params)
        else:
            item.price = params['price']
            item.store_id = params['store_id']
        item.save_to_db()
        return item.json()


def parse_params():
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="Price cannot be blank")
    parser.add_argument("store_id", type=int, required=True, help="Every item needs a store id")
    return parser.parse_args()
