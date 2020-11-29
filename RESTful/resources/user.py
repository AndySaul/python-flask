from flask_restful import Resource, reqparse

from models.user import User


class RegisterUser(Resource):

    def post(self):
        params = self._parse_params()
        if User.find_by_username(params['username']):
            return {'message': "User already registered"}, 400

        user = User(**params)
        user.save_to_db()
        return {'message': "User created successfully"}, 201

    @staticmethod
    def _parse_params():
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        return parser.parse_args()
