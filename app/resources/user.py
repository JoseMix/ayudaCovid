from flask import redirect, render_template, request, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import User
from app.helpers.auth import authenticated

# Protected resources
def index():
    if not authenticated(session):
        abort(401)
    conn = SQLAlchemy()
    users = User.all(conn)
    print("HOOOLAA")
    print(users)
    return render_template("user/index.html", users=users)


def show():
    if not authenticated(session):
        abort(401)
    user = User().find_by_id(1)
    print(user)
    return render_template("user/show.html", user=user)


def new():
    if not authenticated(session):
        abort(401)
    return render_template("user/new.html")


def create(form):
    conn = SQLAlchemy()
    # conn = connection()
    user = User()
    user.create(conn, form)
    # Crear y redirigir logueado
    return redirect(url_for("login"))


def validate(form):
    user = User().validate_user_creation(form["email"].data, form["username"].data)
    return user

def eliminar(user_id):
    User().eliminar(id=user_id)
    return render_template("user/eliminar.html")
