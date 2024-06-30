from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(200), index=True, nullable=False)
    user_email = db.Column(db.String(200), index=True, nullable=False)
    user_password = db.Column(db.String(200), index=True, nullable=False)
    

class Admin(UserMixin, db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(200), index=True, nullable=False)
    admin_email = db.Column(db.String(200), index=True, nullable=False)
    admin_password = db.Column(db.String(200), index=True, nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_image = db.Column(db.String(200), nullable=False)
    product_name = db.Column(db.String(200), index=True, nullable=False)
    product_description = db.Column(db.String(500), nullable=False)
    product_price = db.Column(db.String(50), index=True, nullable=False)
    product_category = db.Column(db.String(50), nullable=False)
