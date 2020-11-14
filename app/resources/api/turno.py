from flask import jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy

from app.models.centro import Centro, centro_schema, centros_schema, Turnos, turnos_schema, turno_schema 
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
