from flask import redirect, render_template, request, url_for, session, abort

from app.models.configuracion import Configuracion
from app.helpers.auth import authenticated, tiene_permiso


def update():
    """Actualiza configuracion de sitio"""
    if not authenticated(session) or not tiene_permiso(session, "configuracion_update"):
        abort(401)
    sitio = Configuracion().sitio()
    return render_template("configuracion/update.html", sitio=sitio)


def show():
    """muestra configuracion de sitio"""
    if not authenticated(session) or not tiene_permiso(session, "configuracion_show"):
        abort(401)
    sitio = Configuracion().sitio()
    return render_template("configuracion/show.html", sitio=sitio)


def edit():
    """Muestra formulario de edicion de la configuracion de sitio"""
    if not authenticated(session) or not tiene_permiso(session, "configuracion_update"):
        abort(401)
    Configuracion().edit(formulario=request.form)
    sitio = Configuracion().sitio()
    return render_template("configuracion/show.html", sitio=sitio)
