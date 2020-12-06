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

db = SQLAlchemy()


def show(centro_id):

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
    return ((hora_fin - hora_inicio).total_seconds() / 60) != 30


def new_reserva(centro_id):
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
