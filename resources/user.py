# Copyright (c) Andy Saul 2020

from flask_restful import Resource, reqparse

from models.user import UserModel


class RegisterUser(Resource):

    def post(self):
        params = parse_params()
        if UserModel.find_by_username(params['username']):
            return {'message': "User already registered"}, 400

        user = UserModel(**params)
        user.save_to_db()
        return {'message': "User created successfully"}, 201


def parse_params():
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True)
    parser.add_argument("password", type=str, required=True)
    return parser.parse_args()

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):

        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200

