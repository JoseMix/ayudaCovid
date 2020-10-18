from flask import redirect, render_template, request, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import Configuracion
from app.helpers.auth import authenticated

def update():
    if not authenticated(session):
        abort(401)
    
    sitio = Configuracion.sitio()
    return render_template("configuracion/update.html", sitio=sitio)


def show():
    if not authenticated(session):
        abort(401)
    sitio = Configuracion.sitio()
    return render_template("configuracion/show.html", sitio=sitio)


def edit():
    if not authenticated(session):
        abort(401)
   
    Configuracion.edit(formulario=request.form)
    sitio = Configuracion.sitio()
    return render_template("configuracion/show.html", sitio=sitio)
