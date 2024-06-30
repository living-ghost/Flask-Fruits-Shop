"""
Database Models for Flask Fruits Shop

This module defines the database models for the Flask Fruits Shop application. 
It includes the schema for users, administrators, and products. These models 
are used to interact with the database via SQLAlchemy.

Classes:
- `User`: Represents a user of the application with login credentials.
- `Admin`: Represents an administrator with login credentials and management capabilities.
- `Product`: Represents a product available for purchase, including details like name, price, and description.

Models:
- `User`: User of the application with a username, email, and password.
- `Admin`: Administrator of the application with a username, email, and password.
- `Product`: Product available for sale with an image, name, description, price, and category.

Relationships:
- No relationships between models in this module.
"""

from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    Represents a user in the Flask Fruits Shop application.

    Inherits from `UserMixin` for Flask-Login integration and `db.Model` for SQLAlchemy ORM functionality.

    Attributes:
        id (int): Primary key for the user record.
        user_username (str): The user's username, must be unique and is used for login.
        user_email (str): The user's email address, must be unique.
        user_password (str): The user's password, used for authentication.

    Indexes:
        - `user_username` (Indexed for quick lookup)
        - `user_email` (Indexed for quick lookup)
        - `user_password` (Indexed for quick lookup, though storing passwords should be handled securely)
    """
    id  = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(200), index=True, nullable=False)
    user_email = db.Column(db.String(200), index=True, nullable=False)
    user_password = db.Column(db.String(200), index=True, nullable=False)

class Admin(UserMixin, db.Model):
    """
    Represents an administrator in the Flask Fruits Shop application.

    Inherits from `UserMixin` for Flask-Login integration and `db.Model` for SQLAlchemy ORM functionality.

    Attributes:
        id (int): Primary key for the admin record.
        admin_username (str): The administrator's username, must be unique and is used for login.
        admin_email (str): The administrator's email address, must be unique.
        admin_password (str): The administrator's password, used for authentication.

    Indexes:
        - `admin_username` (Indexed for quick lookup)
        - `admin_email` (Indexed for quick lookup)
        - `admin_password` (Indexed for quick lookup, though storing passwords should be handled securely)
    """
    id  = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(200), index=True, nullable=False)
    admin_email = db.Column(db.String(200), index=True, nullable=False)
    admin_password = db.Column(db.String(200), index=True, nullable=False)

class Product(db.Model):
    """
    Represents a product available for purchase in the Flask Fruits Shop application.

    Attributes:
        id (int): Primary key for the product record.
        product_image (str): URL or path to the product image.
        product_name (str): Name of the product.
        product_description (str): Detailed description of the product.
        product_price (str): Price of the product as a string (consider using a numeric type for prices).
        product_category (str): Category to which the product belongs.

    Indexes:
        - `product_name` (Indexed for quick lookup)
        - `product_price` (Indexed for quick lookup)
    """
    id = db.Column(db.Integer, primary_key=True)
    product_image = db.Column(db.String(200), nullable=False)
    product_name = db.Column(db.String(200), index=True, nullable=False)
    product_description = db.Column(db.String(500), nullable=False)
    product_price = db.Column(db.String(50), index=True, nullable=False)
    product_category = db.Column(db.String(50), nullable=False)
