from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import RegisterUser
from item import Item, Items


class App(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.secret_key = "super secret key"
        self._api = Api(self)
        self.jwt = JWT(self, authenticate, identity)  # /auth

    def add_resource(self, resource, url):
        self._api.add_resource(resource, url)


app = App()


def main():
    app.add_resource(Items, '/items')
    app.add_resource(Item, '/item/<string:name>')
    app.add_resource(RegisterUser, '/register')
    app.run(port=5000, debug=True)


if __name__ == "__main__":
    main()
