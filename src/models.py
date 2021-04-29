"""
Database schema definition
"""

from enum import Enum

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserType(Base):
    """ Database table for User """
    __tablename__ = "user_types"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    type = sqlalchemy.Column(sqlalchemy.String(256), unique=True)


class User(Base):
    """ Database table for User """
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(256), nullable=True, unique=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    email_validated = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(UserType.id, ondelete='CASCADE'))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=True)

class UserAddress(Base):
    __tablename__ = "user_address"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id, ondelete='CASCADE'))
    address_name = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    last_name = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String(256))
    address = sqlalchemy.Column(sqlalchemy.String(1000))
    country = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    state = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    postal_code = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)

class Category(Base):
    """ Database for categories """
    __tablename__ = "categories"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)


class Product(Base):
    """ Databse table for products """
    __tablename__ = "products"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Category.id, ondelete='CASCADE'))
    name = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String(60), nullable=True)
    discount = sqlalchemy.Column(sqlalchemy.String(60), nullable=True)
    is_available = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    description = sqlalchemy.Column(sqlalchemy.String(2000), nullable=True)
    additional_info = sqlalchemy.Column(sqlalchemy.String(2000), nullable=True)
    seller_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id, ondelete='CASCADE'))


class ProductImages(Base):
    """ Databse table for product_images """
    __tablename__ = "product_images"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Product.id, ondelete='CASCADE'))
    image_url = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    profile_img = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

class ProductReviews(Base):
    """ Databse table for product_reviews """
    __tablename__ = "product_reviews"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Product.id, ondelete='CASCADE'))
    ratings = sqlalchemy.Column(sqlalchemy.SmallInteger, nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=True)


class Cart(Base):
    """ Databse table for cart """
    __tablename__ = "cart"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id, ondelete='CASCADE'))
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Product.id, ondelete='CASCADE'))
    
class Orders(Base):
    """ Databse table for orders """
    __tablename__ = "orders"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id, ondelete='CASCADE'))
    order_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(UserAddress.id, ondelete='CASCADE'))
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Product.id, ondelete='CASCADE'))
    status = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=True)


class ValidationToken(Base):
    """ Database table for validation tokens """
    __tablename__ = 'validation_tokens'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id, ondelete='CASCADE'))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    token = sqlalchemy.Column(sqlalchemy.String(256))
