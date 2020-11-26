from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from src.database import db_session
import src.models as models
from datetime import datetime
import datetime
import time
import threading
import copy
from argon2 import PasswordHasher
import logging
from sqlalchemy import desc

ph = PasswordHasher(hash_len=64, salt_len=32)

admin_view = Blueprint("admin_view", __name__)

@admin_view.route("/add_category")
def add_category():
    pass
    return render_template("admin/add-category.html")

@admin_view.route("/add_product")
def add_product():
    pass
    return render_template("admin/add-product.html")

@admin_view.route("/add_user")
def add_user():
    pass
    return render_template("admin/add-user.html")

@admin_view.route("/categories")
def categories():
    pass
    return render_template("admin/categories.html")

@admin_view.route("/admin_dashboard")
def admin_dashboard():
    pass
    return render_template("admin/index.html")

@admin_view.route("/products")
def products():
    pass
    return render_template("admin/products.html")

@admin_view.route("/users")
def users():
    pass
    return render_template("admin/users.html")
