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
from werkzeug.utils import secure_filename 
import os

ph = PasswordHasher(hash_len=64, salt_len=32)

admin_view = Blueprint("admin_view", __name__)

@admin_view.route("/admin/")
@flask_jwt_extended.jwt_required
def admin_dashboard():
    id = flask_jwt_extended.get_jwt_identity()
    user_type = db_session.query(models.User).filter(models.User.id == int(id)).one_or_none()
    if user_type.user_type_id == 1:
        return redirect(url_for("view.products"))
  
    return render_template("admin/index.html", user_type=user_type.user_type_id)

""" Categories View """

@admin_view.route("/admin/categories")
@flask_jwt_extended.jwt_required
def categories():
    id = flask_jwt_extended.get_jwt_identity()
    user_type = db_session.query(models.User).filter(models.User.id == int(id)).one_or_none()
    if user_type.user_type_id == 1:
        return redirect(url_for("view.products"))
    categories = db_session.query(models.Category).all()
    
    return render_template("admin/categories.html", categories=categories, user_type=user_type.user_type_id)

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
    id = flask_jwt_extended.get_jwt_identity()
    user_type = db_session.query(models.User).filter(models.User.id == int(id)).one_or_none()
    if user_type.user_type_id == 1:
        return redirect(url_for("view.products"))

    if user_type.user_type_id == 3:
        products = db_session.query(models.Product, models.Category).filter(models.Product.category_id == models.Category.id).all()
    else:
        products = db_session.query(models.Product, models.Category).filter(models.Product.category_id == models.Category.id, models.Product.seller_id == int(id)).all()
    
    categories = db_session.query(models.Category).all()
    return render_template("admin/products.html", products=products, categories=categories, user_type=user_type.user_type_id)

@admin_view.route("/admin/add_product")
@flask_jwt_extended.jwt_required
def add_product():
    categories = db_session.query(models.Category).all()
    return render_template("admin/add_product.html", categories=categories)

@admin_view.route("/create_product", methods=["POST"])
@flask_jwt_extended.jwt_required
def create_product():
    try:
        id = flask_jwt_extended.get_jwt_identity()
        
        name = request.form["name"]
        category_id = request.form["category_id"]
        price = request.form["price"]
        discount = request.form["discount"]
        is_available = request.form["is_available"]
        additional_info = request.form["additional_info"]
        description = request.form["description"]

        if is_available == "true":
            is_available = True
        else:
            is_available = False

        create_product = models.Product(category_id=int(category_id), name=name, price=price, discount=discount, is_available=is_available, seller_id=id, description=description, additional_info=additional_info)
        db_session.add(create_product)
        db_session.flush()
        db_session.commit()
    except Exception as e:
        print(e)
        print("failed to create_product")

    try:
        product_image = request.files["product_image"]
        product_other_images = request.files.getlist("product_other_images")
        print(product_image)
        print(product_other_images)
        filename = secure_filename(product_image.filename)
        product_image.save(os.path.join('./static/assets/images/products/', filename))

        profile_image = models.ProductImages(product_id=create_product.id, image_url=str(filename), profile_img=True)
        db_session.add(profile_image)
        db_session.flush()

        for other_images in product_other_images:
            filename = secure_filename(other_images.filename)
            other_images.save(os.path.join('./static/assets/images/products/', filename))
            add_image = models.ProductImages(product_id=create_product.id, image_url=str(filename), profile_img=False)
            db_session.add(add_image)
            db_session.flush()
        
        db_session.commit()
    except Exception as e:
        print(e)

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

@admin_view.route("/admin/users")
@flask_jwt_extended.jwt_required
def users():
    id = flask_jwt_extended.get_jwt_identity()
    user_type = db_session.query(models.User).filter(models.User.id == int(id)).one_or_none()
    if user_type.user_type_id == 1:
        return redirect(url_for("view.products"))

    users = db_session.query(models.User).all()
    user_types = db_session.query(models.UserType).all()
    return render_template("admin/users.html", users=users, user_type=user_type.user_type_id)

@admin_view.route("/create_user", methods=["POST"])
@flask_jwt_extended.jwt_required
def create_user():
    try:
        name = request.form["name"]
        email = request.form["email"]
        password_hash = request.form["password"]
        user_type_id = "1"
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

""" Orders View """

@admin_view.route("/admin/orders")
@flask_jwt_extended.jwt_required
def orders():
    id = flask_jwt_extended.get_jwt_identity()
    
    orders = db_session.query(models.Orders, models.Product, models.User).filter(models.Orders.product_id == models.Product.id, models.Product.seller_id == id, models.User.id == models.Orders.user_id).all()

    return render_template("admin/orders.html", orders=orders)

@admin_view.route("/admin/update_order", methods=["POST"])
@flask_jwt_extended.jwt_required
def update_order():
    id = request.form["id"]
    status = request.form["status"]
    order = db_session.query(models.Orders).filter(models.Orders.id == id).one_or_none()
    if order:
        order.status = status
        db_session.commit()

    return redirect(url_for("admin_view.orders"))