"""
Database schema definition
"""

from enum import Enum

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserTypes(Base):
    """ Database for usertypes """
    __tablename__ = "usertypes"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    type = sqlalchemy.Column(sqlalchemy.SmallInteger, nullable=True)


class User(Base):
    """ Database table for User """
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(256), nullable=True, unique=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    email_validated = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user_type = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(UserTypes.id))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=True)


class Category(Base):
    """ Database for categories """
    __tablename__ = "categories"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)


class Product(Base):
    """ Databse table for products """
    __tablename__ = "products"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Category.id))
    name = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String(60), nullable=True)
    discount = sqlalchemy.Column(sqlalchemy.String(60), nullable=True)
    is_available = sqlalchemy.Column(sqlalchemy.Boolean, default=True)


class ProductImages(Base):
    """ Databse table for product_images """
    __tablename__ = "product_images"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Product.id))
    image_url = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)


class ProductReviews(Base):
    """ Databse table for product_reviews """
    __tablename__ = "product_reviews"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Product.id))
    ratings = sqlalchemy.Column(sqlalchemy.SmallInteger, nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=True)


class Cart(Base):
    """ Databse table for cart """
    __tablename__ = "cart"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id))
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Product.id))


class ValidationToken(Base):
    """ Database table for validation tokens """
    __tablename__ = 'validation_tokens'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    token = sqlalchemy.Column(sqlalchemy.String(256))
