from flask import jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy

from app.models.configuracion import Configuracion, sitio_schema
from marshmallow import ValidationError
from datetime import datetime, timedelta
import re
db = SQLAlchemy()

def sitio():
    try:
        sitio = Configuracion().sitio()

    except:
        response = {
            "message": "Fallo en servidor",
        }
        return jsonify(response), 500

    sitioAPI = sitio_schema.dump(sitio)

    return jsonify({"sitio": sitioAPI}, 200)

