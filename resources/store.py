# Copyright (c) Andy Saul 2020

from flask_restful import Resource
from flask_jwt import jwt_required

from models.store import StoreModel


class Stores(Resource):

    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}


class Store(Resource):

    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name: str):
        if StoreModel.find_by_name(name):
            return {"message": f"Store '{name}' already exists"}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the store."}, 500
        return store.json(), 201

    def delete(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Store deleted"}
