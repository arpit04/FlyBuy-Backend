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
from src.users import verification_mail

ph = PasswordHasher(hash_len=64, salt_len=32)

view = Blueprint("view", __name__)

@view.route("/dashboard")
def dashboard():
    is_login=session.get("logged_in")
    products = [
        {'image':'1.jpg','name':'a','price':'69.00'},
        {'image':'2.jpg','name':'b','price':'79.00'},
        {'image':'3.jpg','name':'c','price':'89.00'},
        {'image':'4.jpg','name':'d','price':'99.00'},
        {'image':'5.jpg','name':'e','price':'109.00'},
        {'image':'6.jpg','name':'f','price':'119.00'},
        {'image':'12.jpg','name':'g','price':'129.00'},
        {'image':'13.jpg','name':'h','price':'139.00'},
    ]
    categories = ["Clothings","Footwears","Electronics","Travel","Toys","Home Living"]
    return render_template("dashboard.html", is_login=is_login,products=products,categories=categories)

@view.route("/product")
def product():
    pass
    return render_template("shop-single-product.html")

@view.route("/home2")
def home2():
    is_login=session.get("logged_in")
    products = [
        {'image':'1.jpg','name':'a','price':'69.00'},
        {'image':'2.jpg','name':'b','price':'79.00'},
        {'image':'3.jpg','name':'c','price':'89.00'},
        {'image':'4.jpg','name':'d','price':'99.00'},
        {'image':'5.jpg','name':'e','price':'109.00'},
        {'image':'6.jpg','name':'f','price':'119.00'},
        {'image':'7.jpg','name':'g','price':'129.00'},
        {'image':'8.jpg','name':'h','price':'139.00'},
        {'image':'9.jpg','name':'i','price':'149.00'},
        {'image':'10.jpg','name':'j','price':'159.00'},
        {'image':'11.jpg','name':'k','price':'169.00'},
        {'image':'12.jpg','name':'l','price':'179.00'},
    ]
    categories = ["Bags","Boot","Clothing","Exclusive","Sandals","Shoes","Sunglasses","Trending","Women"]
    return render_template("shop-right-sidebar.html", is_login=is_login,products=products,categories=categories)

@view.route("/forgot_pass")
def forgot_pass():
    pass
    return render_template("forget-password.html")

@view.route("/reset_pass/<the_token>")
def reset_pass(the_token):
    res, id = verification_mail.update_password(the_token)
    if res and id:
        user = (
            db_session.query(models.User).filter(models.User.id == id).one_or_none()
        )
        return render_template("reset-password.html", email=user.email)

    return render_template("forget-password.html")


@view.route("/")
def user():
    if session.get("logged_in"):
        return redirect(url_for("view.dashboard"))
    return render_template("index.html")


@view.route("/user_logout/")
def user_logout():
    session["logged_in"] = False
    return redirect(url_for("view.user"))


@view.route("/search/", methods=["POST"])
def search():
    print(request.form["search"])
    return redirect(url_for("view.home2"))

@view.route("/user_login/", methods=["POST"])
def user_login():
    email = request.form["email"]
    password = request.form["password"]

    user = (
        db_session.query(models.User).filter(models.User.email == email).one_or_none()
    )
    if user is None:
        return redirect(url_for("view.user"))

    try:
        if ph.verify(user.password_hash, password) and user.email_validated:
            session["logged_in"] = True
            return redirect(url_for("view.dashboard"))
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

@view.route("/register/")
def register():
    if session.get("logged_in"):
        return redirect(url_for("view.dashboard"))
    return render_template("register.html")


@view.route("/registration/", methods=["GET", "POST"])
def registration():
    try:
        name = request.form["name"]
        email = request.form["email"]
        password_hash = request.form["password"]
        print(name, email, password_hash)
        # created_at = datetime.datetime.now()
        # create_user = models.User(
        #     name=name,
        #     email=email,
        #     password_hash=ph.hash(password_hash),
        #     email_validated=False,
        #     created_at=created_at,
        # )
        # db_session.add(create_user)
        # db_session.flush()
    except Exception as e:
        print(e)
        print("failed to create user")
        return redirect(url_for("view.register"))

    # try:
    #     db_session.commit()
    #     res = verification_mail.send_mail(create_user.id, create_user.name, create_user.email, email_type="new-user")
    #     if not res:
    #         print("invalid email or server failed to send verification mail")
    #         return render_template("register.html", message="invalid email or server failed to send verification mail")
    #     return redirect(url_for("view.user"))
    # except Exception as e:
    #     print(e)
    #     print("failed to store user in database")
    #     db_session.rollback()
    #     return redirect(url_for("view.register"))

@view.route("/reset_password/", methods=["GET", "POST"])
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
        return redirect(url_for("view.dashboard"))
    except Exception as e:
        print(e)
        db_session.rollback()
        return redirect(url_for("view.user"))

@view.route("/forgot_password/", methods=["GET", "POST"])
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
            return render_template("register.html", message="user is not registered")
    except Exception as e:
        print(e)
        return redirect(url_for("view.forgot_pass"))

    return redirect(url_for("view.user"))
