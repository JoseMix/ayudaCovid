from flask import redirect, render_template, request, url_for, abort, session, flash
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import User


def login():
    return render_template("auth/login.html")


def authenticate():
    conn = SQLAlchemy()
    # conn = connection()
    params = request.form
    user = User().find_by_email_and_pass(conn, params["email"], params["password"])

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))

    session["user"] = user["email"]
    flash("La sesión se inició correctamente.")

    return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))
