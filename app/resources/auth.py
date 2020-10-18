from flask import redirect, render_template, request, url_for, abort, session, flash
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import User


def login():
    return render_template("auth/login.html")


def authenticate(form):
    conn = SQLAlchemy()
    user = User().find_by_email_and_pass(
        conn, form["email"].data, form["password"].data
    )
    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("login"))
    session["user"] = user["email"]
    session["user_id"] = user["id"]
    
    # return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("home"))


def validate(form):
    conn = SQLAlchemy()
    # conn = connection()
    user = User().validate_user_creation(
        conn, form["email"].data, form["username"].data
    )
    return user