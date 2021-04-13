from app import jwt
from flask import jsonify
from app.resources.user import revoked_tokens

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

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked",
        "error": "token not valid"
    }), 401
