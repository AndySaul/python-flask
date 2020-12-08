# Copyright (c) Andy Saul 2020

import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user import RegisterUser, User, UserLogin, TokenRefresh
from resources.item import Item, Items
from resources.store import Store, Stores

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = "super secret key"
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # TODO: Get admin from db or config
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401


@jwt.revoked_token_loader
def token_revoked():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401


api = Api(app)
api.add_resource(RegisterUser, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Stores, '/stores')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(TokenRefresh, '/refresh')

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


def main():
    app.run(port=5000, debug=True)


if __name__ == "__main__":
    main()
