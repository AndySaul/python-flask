# Copyright (c) Andy Saul 2020

from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_refresh_token_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity)

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


class UserLogin(Resource):

    @classmethod
    def post(cls):
        params = parse_params()
        user = UserModel.find_by_username(params['username'])
        if user and params['password'] == user.password:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        return {'message': 'Invalid credentials'}, 401


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
