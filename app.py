# Copyright (c) Andy Saul 2020

import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.user import RegisterUser, User
from resources.item import Item, Items
from resources.store import Store, Stores

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = "super secret key"
jwt = JWT(app, authenticate, identity)  # /auth

api = Api(app)
api.add_resource(RegisterUser, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Stores, '/stores')
api.add_resource(Store, '/store/<string:name>')

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


def main():
    app.run(port=5000, debug=True)


if __name__ == "__main__":
    main()
