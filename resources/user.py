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
