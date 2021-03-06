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
import flask_jwt_extended
import os

ph = PasswordHasher(hash_len=64, salt_len=32)

admin_view = Blueprint("admin_view", __name__)

@admin_view.route("/admin_dashboard/")
@flask_jwt_extended.jwt_required
def admin_dashboard():
    # if not session.get("logged_in"):
    #     return render_template("index.html")
    return render_template("admin/index.html")

""" Categories View """

@admin_view.route("/categories")
@flask_jwt_extended.jwt_required
def categories():
    # if not session.get("logged_in"):
    #     return render_template("index.html")
    categories = db_session.query(models.Category).all()
    return render_template("admin/categories.html", categories=categories)

@admin_view.route("/create_category", methods=["POST"])
@flask_jwt_extended.jwt_required
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
    return redirect(url_for("admin_view.categories"))

@admin_view.route("/update_category", methods=["POST"])
@flask_jwt_extended.jwt_required
def update_category():
    id = request.form["id"]
    category_name = request.form["category_name"]
    category = db_session.query(models.Category).filter(models.Category.id == int(id)).one_or_none()
    if category:
        category.name = category_name
        db_session.commit()
    return redirect(url_for("admin_view.categories"))

@admin_view.route("/delete_category/<category_id>")
@flask_jwt_extended.jwt_required
def delete_category(category_id):
    category = db_session.query(models.Category).filter(models.Category.id == int(category_id)).one_or_none()
    db_session.delete(category)
    db_session.commit()

    return redirect(url_for("admin_view.categories"))

""" Product View """

@admin_view.route("/admin/products")
@flask_jwt_extended.jwt_required
def products():
    # if not session.get("logged_in"):
    #     return render_template("index.html")
    products = db_session.query(models.Product, models.Category).filter(models.Product.category_id == models.Category.id).all()
    categories = db_session.query(models.Category).all()
    return render_template("admin/products.html", products=products, categories=categories)

@admin_view.route("/create_product", methods=["POST"])
@flask_jwt_extended.jwt_required
def create_product():
    try:
        name = request.form["name"]
        category_id = request.form["category_id"]
        price = request.form["price"]
        discount = request.form["discount"]
        is_available = request.form["is_available"]

        if is_available == "true":
            is_available = True
        else:
            is_available = False

        create_product = models.Product(category_id=int(category_id), name=name, price=price, discount=discount, is_available=is_available)
        db_session.add(create_product)
        db_session.flush()
        db_session.commit()
    except Exception as e:
        print(e)
        print("failed to create_product")
    return redirect(url_for("admin_view.products"))

@admin_view.route("/update_product", methods=["POST"])
@flask_jwt_extended.jwt_required
def update_product():
    id = request.form["id"]
    name = request.form["name"]
    category_id = request.form["category_id"]
    price = request.form["price"]
    discount = request.form["discount"]

    product = db_session.query(models.Product).filter(models.Product.id == int(id)).one_or_none()
    if product:
        product.name = name
        product.category_id = int(category_id)
        product.price = price
        product.discount = discount

        db_session.commit()
    return redirect(url_for("admin_view.products"))

@admin_view.route("/delete_product/<product_id>")
@flask_jwt_extended.jwt_required
def delete_product(product_id):
    product = db_session.query(models.Product).filter(models.Product.id == int(product_id)).one_or_none()
    db_session.delete(product)
    db_session.commit()

    return redirect(url_for("admin_view.products"))

@admin_view.route("/product_images/<product_id>")
def product_images(product_id):
    images = db_session.query(models.ProductImages).filter(models.ProductImages.product_id == int(product_id)).all()

    return render_template("admin/product_images.html", images=images, product_id=product_id)

@admin_view.route("/upload_images", methods=["POST"])
def upload_images():
    UPLOAD_FOLDER = r'static\assets\images\products'
    try:
        product_id = request.form["product_id"]
        uploaded_files = request.files.getlist("image")

        for file in uploaded_files:
            product_images = models.ProductImages(product_id=int(product_id), image_url=file.filename)
            db_session.add(product_images)
            db_session.flush()
            db_session.commit()
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    except Exception as e:
        print(e)
        print("failed to save product_images")

    return redirect(url_for("admin_view.product_images", product_id=product_id))

""" Users View """

@admin_view.route("/users")
@flask_jwt_extended.jwt_required
def users():
    # if not session.get("logged_in"):
    #     return render_template("index.html")
    users = db_session.query(models.User).all()
    user_types = db_session.query(models.UserType).all()
    return render_template("admin/users.html", users=users, user_types=user_types)

@admin_view.route("/create_user", methods=["POST"])
@flask_jwt_extended.jwt_required
def create_user():
    try:
        name = request.form["name"]
        email = request.form["email"]
        password_hash = request.form["password"]
        user_type_id = request.form["user_type_id"]
        created_at = datetime.datetime.now()
        create_user = models.User(
            name=name,
            email=email,
            password_hash=ph.hash(password_hash),
            email_validated=True,
            user_type_id=user_type_id,
            created_at=created_at,
        )
        db_session.add(create_user)
        db_session.flush()
    except Exception as e:
        print(e)
        print("failed to create user")
        return redirect(url_for("admin_view.users"))

    try:
        db_session.commit()
    except Exception as e:
        print(e)
        print("failed to store user in database")
        db_session.rollback()

    return redirect(url_for("admin_view.users"))

@admin_view.route("/update_user", methods=["POST"])
@flask_jwt_extended.jwt_required
def update_user():
    id = request.form["id"]
    name = request.form["name"]
    email = request.form["email"]
    user_type_id = request.form["user_type_id"]

    user = db_session.query(models.User).filter(models.User.id == int(id)).one_or_none()
    if user:
        user.name = name
        user.user_type_id = user_type_id

        db_session.commit()
    return redirect(url_for("admin_view.users"))

@admin_view.route("/delete_user/<user_id>")
@flask_jwt_extended.jwt_required
def delete_user(user_id):
    user = db_session.query(models.User).filter(models.User.id == int(user_id)).one_or_none()
    db_session.delete(user)
    db_session.commit()
    return redirect(url_for("admin_view.users"))
