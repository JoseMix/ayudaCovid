from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.auth import authenticated
from app.models.centro import Bloque, Centro, Turnos
from datetime import date
import datetime

#listado de turnos de centro X
def index():
    if not authenticated(session):
        abort(401)
    turnos = Turnos().all()
    #print(turnos)
    #print(date.today() + datetime.timedelta(days = 2))
    if request.method == 'POST':
        True #realiza busqueda de turnos con datos del request.form
    return render_template("turnos/index.html", turnos=turnos)


#provisorio para cargar bloque de turnos
def horario():
    Turnos().create(request.form)
    flash("hora ok")
    return render_template("turnos/index.html")


def new():
    if not authenticated(session):
        abort(401)
    
    centro = Centro().find_by_id(request.args.get("centro_id"))
    bloques = Bloque().all()
    return render_template("turnos/new.html", centro=centro, bloques=bloques)

#falta validar datos
def create():
    Turnos().create(request.form)
    return render_template("turnos/index.html")

def eliminar():
    return True
    #render_template("")