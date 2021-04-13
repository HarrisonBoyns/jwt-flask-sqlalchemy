from app.database.db import db

# sql alchemy handles the connection and can build the queries. Can be used to find the data for you
# and autromatically returns some data

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship('StoreModel')

    def __init__(self, item, price, store_id):
        self.item = item
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"id":self.id,
                "name": self.item,
                "price": self.price,
                "store_id": self.store_id
                }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(item=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def delete_all(cls):
        return cls.query.delete()