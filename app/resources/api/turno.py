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
from datetime import datetime

db = SQLAlchemy()


def show(centro_id, fecha=datetime.today().strftime("%Y-%m-%d")):
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
        datetime.strptime(fecha, "%Y-%m-%d")
    except:
        response = {
            "message": "La fecha no es valida, el formato debe ser AAAA-mm-dd",
        }
        return jsonify(response), 404

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
    return jsonify({"turno": result, "centro_id": centro_id, "fecha": fecha}, 200)
