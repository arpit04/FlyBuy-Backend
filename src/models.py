"""
Database schema definition
"""

from enum import Enum

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """ Database table for User """
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(256), nullable=True, unique=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    email_validated = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=True)


class ValidationToken(Base):
    """ Database table for validation tokens """
    __tablename__ = 'validation_tokens'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime())
    token = sqlalchemy.Column(sqlalchemy.String(256)) 
