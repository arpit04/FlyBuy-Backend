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

@admin_view.route("/admin/")
def admin():
    if session.get("logged_in"):
        return redirect(url_for("admin_view.admin_dashboard"))
    return render_template("admin/admin_login.html")

@admin_view.route("/admin_logout/")
def admin_logout():
    session["logged_in"] = False
    return redirect(url_for("admin_view.admin"))

@admin_view.route("/admin_login", methods=["POST"])
def admin_login():
    email = request.form["email"]
    password = request.form["password"]

    admin = (
        db_session.query(models.Admin).filter(models.Admin.email == email).one_or_none()
    )
    if admin is None:
        return redirect(url_for("admin_view.admin"))

    try:
        if ph.verify(admin.password_hash, password):
            session["logged_in"] = True
            return redirect(url_for("admin_view.admin_dashboard"))
    except Exception as e:
        print(e)

    return redirect(url_for("admin_view.admin"))

@admin_view.route("/signup/")
def signup():
    return render_template("admin/admin_signup.html")

@admin_view.route("/admin_signup", methods=["POST"])
def admin_signup():
    try:
        email = request.form["email"]
        password_hash = request.form["password"]
        create_admin = models.Admin(
            email=email,
            password_hash=ph.hash(password_hash),
        )
        db_session.add(create_admin)
        db_session.flush()
        db_session.commit()
    except Exception as e:
        print(e)
        print("failed to create user")
        return redirect(url_for("admin_view.admin"))
    return redirect(url_for("admin_view.admin"))

@admin_view.route("/admin_dashboard/")
def admin_dashboard():
    pass
    return render_template("admin/index.html")

""" Categories View """

@admin_view.route("/categories")
def categories():
    categories = db_session.query(models.Category).all()
    return render_template("admin/categories.html", categories=categories)

@admin_view.route("/add_category")
def add_category():
    return render_template("admin/add-category.html")

@admin_view.route("/create_category", methods=["POST"])
def create_category():
    try:
        name = request.form["name"]

        create_category = models.Category(name=name)
        db_session.add(create_category)
        db_session.flush()
        db_session.commit()
    except Exception as e:
        print(e)
        print("failed to create_category")
        return redirect(url_for("admin_view.add_category"))
    return redirect(url_for("admin_view.categories"))

@admin_view.route("/update_category", methods=["POST"])
def update_category():
    id = request.form["id"]
    category_name = request.form["category_name"]
    category = db_session.query(models.Category).filter(models.Category.id == int(id)).one_or_none()
    if category:
        category.name = category_name
        db_session.commit()
    return redirect(url_for("admin_view.categories"))

@admin_view.route("/delete_category/<category_id>")
def delete_category(category_id):
    category = db_session.query(models.Category).filter(models.Category.id == int(category_id)).one_or_none()
    db_session.delete(category)
    db_session.commit()

    return redirect(url_for("admin_view.categories"))
""" Product View """

@admin_view.route("/products")
def products():
    pass
    return render_template("admin/products.html")

@admin_view.route("/add_product")
def add_product():
    pass
    return render_template("admin/add-product.html")

""" Users View """

@admin_view.route("/users")
def users():
    pass
    return render_template("admin/users.html")

@admin_view.route("/add_user")
def add_user():
    pass
    return render_template("admin/add-user.html")
