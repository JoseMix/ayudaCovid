from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.auth import authenticated, tiene_permiso
from app.models.centro import Bloque, Centro, Turnos
from datetime import date
import datetime
import time


def new():

    """redirecciona al formulario de alta de turno y lógica del POST """
    if not authenticated(session) or not tiene_permiso(session, "turnos_new"):
        abort(401)
    centro = Centro().find_by_id(request.args.get("centro_id"))
    if centro.activo == False:
        abort(401)
    bloques = Bloque().all()
    rango = {}
    rango["inicio"] = date.today()
    rango["fin"] = date.today() + datetime.timedelta(days=2)
    form = request.form
    if request.method == "POST":
        if create():
            return redirect(url_for("centro_show", centro_id=centro.id))
    return render_template(
        "turnos/new.html", centro=centro, bloques=bloques, rango=rango, form=form
    )


def create():
    """ valida datos del formulario y crea el turno """
    centro_id = request.form["centro_id"]
    if fecha_turno_valido(request.form) and validar_horario_inicio(request.form):
        Turnos().create(request.form)
        flash("¡Turno asignado exitosamente!")
        return True
    else:
        return False


def fecha_turno_valido(form):
    """ valida que no exista turno """
    bloque = Turnos().find_by(form["dia"], form["bloque"], form["centro_id"])
    if bloque:
        flash(
            "El horario seleccionado para el día seleccionado se encuentra reservado."
        )
        return False
    else:
        return True


def validar_horario_inicio(form):
    """ valida que el horario y dia seleccionado no sea el actual o pasado. retorna boolean """
    if form["dia"] == str(date.today()):
        bloque = Bloque().find_by_id(form["bloque"])
        hh_act = time.localtime().tm_hour
        mm_act = time.localtime().tm_min
        if bloque.hora_inicio.hour <= hh_act:
            flash("El horario seleccionado para el día de hoy ya no está vigente")
            return False
    return True


def eliminar():
    """cancela un turno segun id"""
    if not authenticated(session) or not tiene_permiso(session, "turnos_destroy"):
        abort(401)
    Turnos().eliminar(request.args.get("turno_id"))
    flash("El turno se canceló exitosamente")
    return redirect(
        url_for(
            "centro_show",
            centro_id=request.args.get("centro_id"),
            page=request.args.get("page"),
            email=request.args.get("email"),
        )
    )
