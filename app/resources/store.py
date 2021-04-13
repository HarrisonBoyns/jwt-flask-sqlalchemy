from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from app.models.store_model import StoreModel

class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="include name field")

    @jwt_required()
    def get(self, name):
        json_item = StoreModel.find_by_name(name)
        if json_item is None:
            return {"message":"item not found"}, 404
        return {"store": json_item.json()}

    @jwt_required()
    def post(self, name):

        json_item = StoreModel.find_by_name(name)
        if json_item is not None:
            return {"message": "item with this name already exists"}, 404
        data = Store.parser.parse_args()
        user_model = StoreModel(data.get("name"))
        try:
            user_model.save_to_db()
        except:
            return {"message":"server error"}, 500
        return user_model.json(), 201

    @jwt_required()
    def delete(self, name):
        json_item = StoreModel.find_by_name(name)

        if json_item is None:
            return {"message": "item not found"}, 400
        json_item.delete_from_db()
        return {"message": "deleted"}, 201

    @jwt_required()
    def put(self, name):
        data = Store.parser.parse_args()
        json_item = StoreModel.find_by_name(name)
        if json_item is None:
            json_item = StoreModel(name)
        else:
            json_item.name = data["name"]
        json_item.save_to_db()
        return {"item": data}, 200


class StoreList(Resource):

    @jwt_required()
    def get(self):
        return {"stores": [item.json() for item in StoreModel.get_all()]}, 200

    @jwt_required()
    def delete(self):
        StoreModel.delete_all()
        return {"message": "success"}, 200
