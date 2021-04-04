from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
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
from src.users import verification_mail
import flask_jwt_extended

ph = PasswordHasher(hash_len=64, salt_len=32)

view = Blueprint("view", __name__)

@view.route("/checkout")
@flask_jwt_extended.jwt_required
def checkout():
    pass
    return render_template("checkout.html")

@view.route("/payment")
@flask_jwt_extended.jwt_required
def payment():
    pass
    return render_template("payment.html")


@view.route("/cart")
@flask_jwt_extended.jwt_required
def cart():
    user_id = flask_jwt_extended.get_jwt_identity()
    cart_list = db_session.query(models.Cart, models.Product).filter(models.Cart.product_id == models.Product.id).filter(models.Cart.user_id == user_id).all()
   
    return render_template("cart.html", cart_list=cart_list, cart_count=len(cart_list))

@view.route("/add_to_cart/<product_id>")
@flask_jwt_extended.jwt_required
def add_to_cart(product_id):
    user_id = flask_jwt_extended.get_jwt_identity()
    try:
        if product_id != "0":
            add_to_cart = models.Cart(user_id=user_id, product_id=product_id)
            db_session.add(add_to_cart)
            db_session.flush()
            db_session.commit()
    except Exception as e:
        print(e)

    return redirect(url_for("view.cart"))


@view.route("/cart_remove/<int:cart_id>")
@flask_jwt_extended.jwt_required
def cart_remove(cart_id):
    try:
        cart_item = db_session.query(models.Cart).filter(models.Cart.id == cart_id).one_or_none()
        db_session.delete(cart_item)
        db_session.commit()
    except Exception as e:
        print(e)

    return redirect(url_for("view.cart"))

@view.route("/product/<id>")
@flask_jwt_extended.jwt_required
def product(id):
    try:
        product = db_session.query(models.Product).filter(models.Product.id == id).one_or_none()
    except Exception as e:
        print(e)

    return render_template("shop-single-product.html", product=product)

@view.route("/products")
@flask_jwt_extended.jwt_required
def products():
    try:
        user_id = flask_jwt_extended.get_jwt_identity()
        is_login = session.get("logged_in")
        products = db_session.query(models.Product, models.Category).filter(models.Product.category_id == models.Category.id).all()
        categories = db_session.query(models.Category).all()
        cart_count = db_session.query(models.Cart, models.Product).filter(models.Cart.product_id == models.Product.id).filter(models.Cart.user_id == user_id).count()
    except Exception as e:
        print(e)

    return render_template("shop-right-sidebar.html", is_login=is_login,products=products,categories=categories, cart_count=cart_count)

@view.route("/forgot_pass")
@flask_jwt_extended.jwt_required
def forgot_pass():
    pass
    return render_template("forget-password.html")

@view.route("/reset_pass/<the_token>")
def reset_pass(the_token):
    try:
        res, id = verification_mail.update_password(the_token)
        if res and id:
            user = (
                db_session.query(models.User).filter(models.User.id == id).one_or_none()
            )
            return render_template("reset-password.html", email=user.email)
    except Exception as e:
        print(e)

    return render_template("forget-password.html")


@view.route("/")
def user():
    if session.get("logged_in"):
        return redirect(url_for("view.products"))
    return render_template("index.html")


@view.route("/user_logout")
def user_logout():
    resp = redirect(url_for("view.user"))
    flask_jwt_extended.unset_access_cookies(resp)
    return resp


@view.route("/search", methods=["POST"])
def search():
    print(request.form["search"])
    return redirect(url_for("view.products"))

@view.route("/user_login", methods=["POST"])
def user_login():
    email = request.form["email"]
    password = request.form["password"]
    user = (
        db_session.query(models.User).filter(models.User.email == email).one_or_none()
    )
    if user is None:
        return "no user found", 400
    try:
        if ph.verify(user.password_hash, password) and user.email_validated:
            access_token = flask_jwt_extended.create_access_token(identity=user.id)
            resp = jsonify(success=True)
            flask_jwt_extended.set_access_cookies(resp, access_token)
            return resp
    except Exception as e:
        print(e)

    return redirect(url_for("view.user"))

@view.route("/validate_user/<the_token>")
def validate_user(the_token):
    res = verification_mail.validate_email(the_token)
    if not res:
        message = "verification failed <br><span> link expired or invalid token</span>"
        return render_template("user_verification.html", message=message)

    message = "Thanks for registration <br><span> Now you can access your account</span>"
    return render_template("user_verification.html", message=message)

@view.route("/register")
def register():
    if session.get("logged_in"):
        return redirect(url_for("view.products"))
    user_types = db_session.query(models.UserType).all()
    return render_template("register.html",user_types=user_types)


@view.route("/registration", methods=["GET", "POST"])
def registration():
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
            email_validated=False,
            user_type_id=user_type_id,
            created_at=created_at,
        )
        db_session.add(create_user)
        db_session.flush()
    except Exception as e:
        print(e)
        print("failed to create user")
        return redirect(url_for("view.register"))

    try:
        db_session.commit()
        res = verification_mail.send_mail(create_user.id, create_user.name, create_user.email, email_type="new-user")
        if not res:
            print("invalid email or server failed to send verification mail")
            return redirect(url_for("view.register"))
        return redirect(url_for("view.user"))
    except Exception as e:
        print(e)
        print("failed to store user in database")
        db_session.rollback()
        return redirect(url_for("view.register"))

@view.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    try:
        email = request.form["email"]
        password_hash = request.form["password"]

        user = (
            db_session.query(models.User).filter(models.User.email == email).one_or_none()
        )
        user.password_hash = ph.hash(password_hash)
    except Exception as e:
        print(e)
        return {"message": "Failed to get user"}

    try:
        db_session.commit()
        session["logged_in"] = True
        return redirect(url_for("view.products"))
    except Exception as e:
        print(e)
        db_session.rollback()
        return redirect(url_for("view.user"))

@view.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    try:
        email = request.form["email"]
        user = (
            db_session.query(models.User).filter(models.User.email == email).one_or_none()
        )
        if user:
            res = verification_mail.send_mail(user.id, user.name, user.email, email_type="reset-user")
            if not res:
                return render_template("index.html", message="invalid email or server failed to send verification mail")
        else:
            return redirect(url_for("view.register"))
    except Exception as e:
        print(e)
        return redirect(url_for("view.forgot_pass"))

    return redirect(url_for("view.user"))
