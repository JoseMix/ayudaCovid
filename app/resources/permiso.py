from flask import redirect, render_template, request, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import Permiso, Configuracion
from app.helpers.auth import authenticated

# Public resources
def index():
    if not authenticated(session):
        abort(401)
    conn = SQLAlchemy()
    # conn = connection()
    permisos = Permiso.all(conn)
    sitio = Configuracion.sitio()
    return render_template("permiso/index.html", permisos=permisos, sitio=sitio)


def new():
    if not authenticated(session):
        abort(401)
    sitio = Configuracion.sitio()
    return render_template("permiso/new.html", sitio=sitio)


def create():
    if not authenticated(session):
        abort(401)
    conn = SQLAlchemy()
    # conn = connection()
    Permiso.create(conn, request.form)
    sitio = Configuracion.sitio()
    return redirect(url_for("permiso_index", sitio=sitio))
