from flask import redirect, render_template, request, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import Configuracion
from app.helpers.auth import authenticated

def new():
    if not authenticated(session):
        abort(401)
    return render_template("configuracion/new.html")

'''
def show():
    if not authenticated(session):
        abort(401)
    conn = SQLAlchemy()
    sitio = Configuracion.sitio(conn)
    return render_template("configuracion/show.html", sitio=sitio)
'''

def create():
    if not authenticated(session):
        abort(401)
    conn = SQLAlchemy()
    Configuracion.create(conn, request.form)
    return render_template("configuracion/new.html")
