from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from app.models.item_model import ItemModel

class Items(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="include name field")
    parser.add_argument('price', type=float, required=True, help="include price field")
    parser.add_argument('store_id', type=float, required=True, help="include store_id field")

    @jwt_required()
    def get(self, name):
        json_item = ItemModel.find_by_name(name)
        print(json_item)
        if json_item is None:
            return {"message":"item not found"}, 404
        print(json_item)
        return {"item": json_item.json()}

    @jwt_required(fresh=True)
    def post(self, name):
        json_item = ItemModel.find_by_name(name)
        if json_item is not None:
            return {"message": "item with this name already exists"}, 404
        data = Items.parser.parse_args()
        user_model = ItemModel(data.get("name"), data.get("price"), data.get("store_id"))
        user_model.save_to_db()
        return user_model.json(), 201

    @jwt_required()
    def delete(self, name):
        json_item = ItemModel.find_by_name(name)

        if json_item is None:
            return {"message": "item not found"}, 400

        json_item.delete_from_db()
        return {"message": "deleted"}, 201

    @jwt_required()
    def put(self, name):
        data = Items.parser.parse_args()
        json_item = ItemModel.find_by_name(name)
        if json_item is None:
            json_item = ItemModel(name, data["price"])
        else:
            json_item.price = data["price"]
        json_item.save_to_db()
        return {"item": data}, 200


class ItemList(Resource):

    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = {"items": [item.json() for item in ItemModel.get_all()]}
        if user_id:
            return items, 200
        return {"items": [item["name"]() for item in ItemModel.get_all()],
                "message":"more details available if you log in"}, 200

    @jwt_required()
    def delete(self):

        ItemModel.delete_all()
        return {"message": "success"}, 200
