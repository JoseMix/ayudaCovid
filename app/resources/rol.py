from flask import redirect, render_template, request, url_for, session, abort
from app.models.configuracion import Configuracion
from app.models.models import Rol

from app.helpers.auth import authenticated

# Protected resources
def index():
    if not authenticated(session):
        abort(401)
    
    roles = Rol().all()
    sitio = Configuracion().sitio()
    return render_template("rol/index.html", roles=roles, sitio=sitio)


def new():
    if not authenticated(session):
        abort(401)
    sitio = Configuracion().sitio()
    return render_template("rol/new.html", sitio=sitio)


def create():
    if not authenticated(session):
        abort(401)
    
    Rol().create(request.form)
    sitio = Configuracion().sitio()
    return redirect(url_for("rol_index", sitio=sitio))
