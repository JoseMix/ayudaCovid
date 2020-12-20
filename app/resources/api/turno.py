from flask import jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy

from app.models.centro import (
    Centro,
    Bloque,
    centro_schema,
    centros_schema,
    Turnos,
    turnos_schema,
    turno_schema,
)
from app.models.configuracion import Configuracion
from marshmallow import ValidationError
from datetime import datetime, timedelta
import re
db = SQLAlchemy()


def show(centro_id):
    """Retorna turnos de un centro para una fecha, en caso de no introducir fecha,
    se toma la de hoy y se convierte a formato JSON, segun esquema.
    Se manejan errores si: no existe el centro, la fecha es incorrecta,
    la fecha es anterior al dia de hoy o hay un fallo en el servidor"""
    try:
        centro = Centro().show_one(centro_id)

    except:
        response = {
            "message": "Fallo en servidor",
        }
        return jsonify(response), 500
    if centro is None:
        response = {
            "message": "No existe el centro",
        }
        return jsonify(response), 404
    try:
        fecha = request.args.get("fecha", default=datetime.today().strftime("%d-%m-%Y"))
        datetime.strptime(fecha, "%d-%m-%Y")
    except:
        response = {
            "message": "La fecha no es valida, el formato debe ser dd-mm-AAAA",
        }
        return jsonify(response), 500

    if datetime.strptime(fecha, "%d-%m-%Y") < datetime.now() - timedelta(days=1):
        response = {
            "message": "La fecha es anterior al dia de hoy",
        }
        return jsonify(response), 500

    try:
        turnos = Bloque().bloques_ocupados(centro_id, fecha)
        turnos_all = Bloque().all()

    except:
        response = {
            "message": "Fallo en servidor",
        }
        return jsonify(response), 500

    bloque = []
    for turno in turnos_all:
        if turno not in turnos:
            bloque.append(turno)
    if bloque is None:
        respose = {
            "message": "No existen turnos para ese dia",
        }
        return jsonify(response), 404
    result = turnos_schema.dump(bloque)
    return jsonify({"centro_id": centro_id, "fecha": fecha, "turno": result}, 200)


def es_turno_de_30(hora_inicio, hora_fin):
    """comprueba si la hora ingresada corresponde a 30 minutos"""
    return ((hora_fin - hora_inicio).total_seconds() / 60) != 30

def validate(email): 
       match=re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)",email)
       if not match:
           return 'Email invalido'

def new_reserva(centro_id):
    """Se parsea JSON de un turno y se convierte en un objeto para agregar a la bd.
    Se manejan errores si: falta algun campo, ya existe el turno, si existe un fallo en la bd,
    la fecha no esta en el rango de los 3 dias, o no  son bloques de 30 min"""
    json_data = request.get_json()
    if not json_data:
        response = {
            "message": "No se ingreso ningun dato",
        }
        return jsonify(response), 400
    try:
        data = turno_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    (centro_id, email, nombre, apellido, hora_inicio, hora_fin, fecha, telefono) = (
        centro_id,
        data["email"],
        data["nombre"],
        data["apellido"],
        data["hora_inicio"],
        data["hora_fin"],
        data["fecha"],
        data["telefono"],
    )
    if validate(email):
        response = {
            "message": "Debe ingresar un mail valido",
        }
        return jsonify(response), 500
    obj_fecha = datetime.strftime(fecha, "%d-%m-%Y")
    if datetime.strptime(obj_fecha, "%d-%m-%Y") < datetime.now() - timedelta(
        days=1
    ) or datetime.strptime(obj_fecha, "%d-%m-%Y") > datetime.now() + timedelta(days=2):

        response = {
            "message": "La fecha no esta en el rango de los 3 proximos días",
        }
        return jsonify(response), 500
    if es_turno_de_30(hora_inicio, hora_fin):
        response = {
            "message": "La hora de inicio y fin, deben ser bloques de 30 minutos",
        }
        return jsonify(response), 500
    
    try:
        timeStr = hora_inicio.strftime("%H:%M")
        bloque = Bloque().find_by_hora_inicio(timeStr)
        id_bloque = bloque.id
        turno = Turnos().validar_turno_existente(id_bloque, centro_id, fecha)
    except:
        response = {
            "message": "Fallo en servidor",
        }
        return jsonify(response), 500
    if turno is None:
        turno = Turnos(
            email=email,
            nombre=nombre,
            apellido=apellido,
            dia=fecha,
            turno_id=id_bloque,
            centro_id=centro_id,
            telefono=telefono,
        )
        db.session.add(turno)
        db.session.commit()
        result = turno_schema.dump(turno)
        return jsonify(
            {
                "turno": result,
                "telefono": telefono,
                "hora_inicio": hora_inicio.strftime("%H:%M"),
                "hora_fin": hora_fin.strftime("%H:%M"),
            },
            201,
        )
    else:
        response = {
            "message": "El turno ya existe",
        }
        return jsonify(response), 400


def top(cantidad):
    try:
        top_municipios = Turnos().top(cantidad)
    except:
        response = {
            "message": "Fallo en servidor",
        }
        return jsonify(response), 500

    centrosAPI = []

    centrosAPI.append(turnos_schema.dump(top_municipios))

    return jsonify({"centros": centrosAPI}, 200)


def turnos_por_tipo(fecha_inicio, fecha_fin):
    try:
        turnos = Centro().turnos_por_tipo(fecha_inicio, fecha_fin)
        print(turnos)
    except:
        response = {
            "message": "Fallo en servidor",
        }
        return jsonify(response), 500

    turnosAPI = []

    turnosAPI.append(centros_schema.dump(turnos))

    return jsonify({"centros": turnosAPI}, 200)
