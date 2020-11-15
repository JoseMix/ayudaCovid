from flask import jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy

from app.models.centro import Centro, Bloque, centro_schema, centros_schema, Turnos, turnos_schema, turno_schema
from app.models.configuracion import Configuracion
from marshmallow import ValidationError
from datetime import datetime
db = SQLAlchemy()



def show(centro_id,fecha=datetime.today().strftime('%Y-%m-%d')):
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
        turnos = Turnos().turno_centro_fecha(centro_id, fecha)
    except:
        response = {
            "message": "Fallo en servidor turno",
        }
        return jsonify(response), 500    
    if turnos is None:
        respo = {
            "message": "No existen turnos para ese dia",
        }
        return jsonify(respo), 404    
    result = turnos_schema.dump(turnos)
    return jsonify({"turno": result}, 200)


def new_reserva():
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
    (
        centro_id,
        email_donante,
        hora_inicio,
        hora_fin,
        fecha,
    ) = (
        data["centro_id"],
        data["email_donante"],
        data["hora_inicio"],
        data["hora_fin"],
        data["fecha"],
    )

    try:
        bloque = Bloque().find_by_hora_inicio(hora_inicio="14:00")
        id_bloque = bloque.id
        turno = Turnos().validar_turno_existente(bloque.id,'2',"2020-11-16")
    except:
        response = {
            "message": "Fallo en servidor",
        }
        return jsonify(response), 500
    if turno is None:
        turno = Turnos(
            email = email_donante,
            dia=fecha,
            turno_id=id_bloque,
            centro_id='2'
        )
        db.session.add(turno)
        db.session.commit()
        result = turno_schema.dump(turno)
        return jsonify({"turno": result}, 201)
    else:
        response = {
            "message": "El turno ya existe",
        }
        return jsonify(response), 400