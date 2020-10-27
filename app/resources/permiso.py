from flask import redirect, render_template, request, url_for, session, abort
from app.models.models import Permiso
from app.models.configuracion import Configuracion

from app.helpers.auth import authenticated

# Public resources
def index(page=1):
    if not authenticated(session):
        abort(401)
    sitio = Configuracion().sitio()
    index_pag = Permiso().all_paginado(page, sitio.paginas)
    return render_template("permiso/index.html", index_pag=index_pag, sitio=sitio)


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
