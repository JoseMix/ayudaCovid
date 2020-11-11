from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.auth import authenticated
from app.models.centro import Turnos


#listado de turnos de centro X
def index():
    if not authenticated(session):
        abort(401)
    if request.method == 'POST':
        horario()#
    return render_template("turnos/index.html")

#provisorio para cargar bloque de turnos
def horario():
    Turnos().create(request.form)
    flash("hora ok")
    return render_template("turnos/index.html")