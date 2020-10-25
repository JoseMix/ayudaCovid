from flask import redirect, render_template, request, url_for, session, abort
from app.models.models import Permiso
from app.models.configuracion import Configuracion

from app.helpers.auth import authenticated

# Public resources
def index():
    if not authenticated(session):
        abort(401)
   
    permisos = Permiso().all()
    sitio = Configuracion().sitio()
    return render_template("permiso/index.html", permisos=permisos, sitio=sitio)


def new():
    if not authenticated(session):
        abort(401)
    sitio = Configuracion().sitio()
    return render_template("permiso/new.html", sitio=sitio)


def create():
    if not authenticated(session):
        abort(401)
    Permiso().create(request.form)
    sitio = Configuracion().sitio()
    return redirect(url_for("permiso_index", sitio=sitio))
