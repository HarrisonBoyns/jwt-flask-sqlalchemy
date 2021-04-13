from flask_jwt_extended import (jwt_required,
                                get_jwt,
                                create_access_token,
                                create_refresh_token
                                )
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from app.models.user_model import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="password field cannot be blank"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="username field cannot be blank"
                          )

revoked_tokens = []

class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])

        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200
        return {"message": "invalid credentials"}, 401


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        item = UserModel.find_by_username(data["username"])
        if item:
            return {"message": "username already exists"}, 400

        user = UserModel(**data)
        user.save()
        return {"message": "user created successfully"}

class AllUsers(Resource):

    def get(self):
        return [user.json() for user in UserModel.find_all()]

class UserResource(Resource):

    def get(self, id):
        user = UserModel.find_by_id(id)
        if user:
            return user.json()
        else:
            return {"message": "user does not exist"}, 404

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        print(claims)
        if not claims['is_admin']:
            return {"message": "admin privilege required"}
        user = UserModel.find_by_id(id)
        if user:
            user.delete()
            return {"message": "user deleted"}, 200
        else:
            return {"message": "user not found"}, 404


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        user = get_jwt()
        # not fresh --> not sure whether they have just logged in --> adds to security
        new_access_token = create_access_token(identity=user, fresh=False)
        return {"access_token": new_access_token}, 200


class UserLogOut(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        revoked_tokens.append(jti)
        return {"message": "logged out"}
