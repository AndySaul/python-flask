from flask_restful import Resource, reqparse

from resources.database import Database
from models.user import User


class RegisterUser(Resource):

    def post(self):
        params = self._parse_params()
        if User.find_by_username(params['username']):
            return {'message': "User already registered"}, 400

        with Database() as db:
            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            args = (params['username'], params['password'])
            db.execute(query, args)
        return {'message': "User created successfully"}, 201

    @staticmethod
    def _parse_params():
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        return parser.parse_args()
