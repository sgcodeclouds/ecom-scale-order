from app.extensions import db
from sqlalchemy import inspect
from sqlalchemy.orm import validates

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_id = db.Column(db.String(500))
    items = db.Column(db.Text)
    order_total=db.Column(db.Float)
    user_id=db.Column(db.String(500))
    
    @validates('user_id')
    def validate_userid(self, key, value):
        if not value or value == "":
            raise ValueError("Must have a user id")
        return value

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


    def __repr__(self):
        return f'<Order "{self.product_id}">'