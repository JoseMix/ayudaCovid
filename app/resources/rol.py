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
    #acá falta hacer el paginado para los roles
    return render_template("rol/index.html", roles=roles, sitio=sitio)

def new():
    if not authenticated(session):
        abort(401)
    return render_template("rol/new.html")


def create():
    if not authenticated(session):
        abort(401)
    Rol().create(request.form)
    roles = Rol().all()

    return render_template("rol/index.html", roles=roles)
