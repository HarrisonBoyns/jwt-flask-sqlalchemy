from app.database.db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.Column(db.String(80))

    items = db.relationship("ItemModel", lazy="dynamic")

    # why use lazy dynamic -- > creates a query builder and therefore we have an option

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "items": [item.json() for item in self.items.all()]
                }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

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
