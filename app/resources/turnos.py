from flask import redirect, render_template, request, url_for, session, abort, flash
from app.helpers.auth import authenticated, tiene_permiso
from app.models.centro import Bloque, Centro, Turnos
from datetime import date
import datetime


# redirecciona al formulario de alta de turno y lógica del POST 
def new():
    if not authenticated(session)or not tiene_permiso(session, 'turnos_new'):
        abort(401)
    centro = Centro().find_by_id(request.args.get("centro_id"))
    if(centro.activo == False ):
        abort(401)
    bloques = Bloque().all()
    rango= {}
    rango["inicio"] = date.today()
    rango["fin"] = date.today() + datetime.timedelta(days=2)
    form=request.form
    if request.method=="POST":
        if create():
            return redirect(url_for("centro_show", centro_id=centro.id))
    #    else:
    #        return render_template("turnos/new.html", centro=centro, bloques=bloques, rango=rango, form=form)
    #else:
    return render_template("turnos/new.html", centro=centro, bloques=bloques, rango=rango, form=form)


#valida datos y crea el turno
def create():
    centro_id=request.form["centro_id"]
    if fecha_turno_valido(request.form):
        Turnos().create(request.form)
        flash("¡Turno asignado exitosamente!")
        return True
    else:
        flash("El horario seleccionado para el día seleccionado se encuentra reservado.")
        return False


#valida que no exista turno 
def fecha_turno_valido(form):
    bloque = Turnos().find_by(form["dia"], form["bloque"], form["centro_id"])
    if bloque:
        return False
    else:
        return True

# or not tiene_permiso(session, 'turnos_destroy')
def eliminar():
    if not authenticated(session) or not tiene_permiso(session, 'turnos_destroy'):
        abort(401)
    Turnos().eliminar(request.args.get("turno_id"))
    flash("El turno se canceló exitosamente")
    return redirect(url_for("centro_show", centro_id=request.args.get("centro_id"), page=request.args.get("page"), email=request.args.get("email")))