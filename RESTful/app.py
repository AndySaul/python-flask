from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.user import RegisterUser, User
from resources.item import Item, Items


class App(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.secret_key = "super secret key"  # todo accept a key string
        self.jwt = JWT(self, authenticate, identity)  # /auth
        self._api = self._init_api()
        self._init_tables()

    def _init_api(self):
        api = Api(self)
        api.add_resource(Items, '/items')
        api.add_resource(Item, '/item/<string:name>')
        api.add_resource(RegisterUser, '/register')
        return api

    def _init_tables(self):
        User.create_table()
        Items.create_table()


def main():
    app = App()
    app.run(port=5000, debug=True)


if __name__ == "__main__":
    main()
