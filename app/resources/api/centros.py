from flask import jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.centro import Centro, centro_schema, centros_schema
from app.models.configuracion import Configuracion
from marshmallow import ValidationError

db = SQLAlchemy()


def index():
    sitio = Configuracion().sitio()
    centros = Centro().all()
    paginado = Centro().all_paginado(1, sitio.paginas)
    pages = paginado.pages
    per_page = paginado.per_page
    if centros is None:
        response = {
            "message": "No existen centros",
        }
        return jsonify(response), 500
    result = centros_schema.dump(centros)
    return jsonify({"centros": result, "pages": pages, "per_page": per_page})


def show_one(centro_id):
    centro = Centro().show_one(centro_id)
    if not centro:
        abort(404)
    result = centro_schema.dump(centro)
    return jsonify({"centro": result}, 200)


def new_centro():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No se ingreso ningun dato"}, 400
    try:
        data = centro_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    (
        apertura,
        cierre,
        direccion,
        email,
        nombre,
        telefono,
        tipo_centro,
        web,
        municipio,
    ) = (
        data["apertura"],
        data["cierre"],
        data["direccion"],
        data["email"],
        data["nombre"],
        data["telefono"],
        data["tipo_centro"],
        data["web"],
        data["municipio"],
    )
    centro = Centro().validate_centro_creation(
        nombre=nombre, direccion=direccion, municipio=municipio
    )
    if centro is None:
        centro = Centro(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            apertura=apertura,
            cierre=cierre,
            tipo_centro=tipo_centro,
            email=email,
            web=web,
            municipio=municipio,
        )
        db.session.add(centro)
        db.session.commit()
        result = centro_schema.dump(centro)
        return jsonify({"centro": result}, 201)
    else:
        response = {
            "message": "El centro ya existe",
        }
        return jsonify(response), 500
