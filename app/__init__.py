from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app.resources.store import StoreList, Store
from app.resources.user import UserRegister, UserResource, UserLogin, TokenRefresh, revoked_tokens, UserLogOut, AllUsers
from app.resources.items import Items, ItemList

app = Flask(__name__)

app.secret_key = "top_secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def is_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in revoked_tokens

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return jsonify({"is_admin": True})
    return {"is_admin": False}


@jwt.expired_token_loader
def expired_token_callback():
    return {
               "description": "The token has expired",
               "error": "token_expired"
           }, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
               "description": "The token is invalid",
               "error": error
           }, 401


@jwt.unauthorized_loader
def invalid_token_callback():
    return {
               "description": "No Token Sent",
               "error": "un_authorised"
           }, 401


@jwt.needs_fresh_token_loader
def refresh_token_callback():
    return jsonify({
        "description": "fresh token required",
        "error": "fresh_token_needed"
    }), 401


# any users that have been logged out
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked",
        "error": "token not valid"
    }), 401

api.add_resource(Items, "/items/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/signup")
api.add_resource(Store, "/stores/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserResource, "/users/<int:id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogOut, "/logout")
api.add_resource(AllUsers, "/users")
