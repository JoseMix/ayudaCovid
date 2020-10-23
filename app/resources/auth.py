from flask import redirect, render_template, request, url_for, abort, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import and_

# from app.db import connection
from app.models.modelos import User


def login():
    return render_template("auth/login.html")


def authenticate(form):
    
    bcrypt = Bcrypt()
    user = (
        User()
        .query.filter(and_(User.email == form.email.data, User.activo == True))
        .first()
    )
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        session["user"] = user["email"]
        session["user_id"] = user["id"]
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))
    # return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("home"))


def validate(form):
    
    user = User().validate_user_creation(
         form["email"].data, form["username"].data
    )
    return user