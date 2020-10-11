from flask import redirect, render_template, request, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import Rol
from app.helpers.auth import authenticated

# Protected resources
def index():
    if not authenticated(session):
        abort(401)
    conn = SQLAlchemy()
    # conn = connection()
    roles = Rol.all(conn)

    return render_template("rol/index.html", roles=roles)


def new():
    if not authenticated(session):
        abort(401)
    return render_template("rol/new.html")


def create():
    if not authenticated(session):
        abort(401)
    conn = SQLAlchemy()
    # conn = connection()
    Rol.create(conn, request.form)

    return redirect(url_for("rol_index"))
