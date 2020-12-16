from flask import jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
import requests
from app.models.centro import Centro, centro_schema, centros_schema
from app.models.configuracion import Configuracion
from marshmallow import ValidationError

db = SQLAlchemy()


def index():
    """Retorna los centros activos, paginados y se convierte en json segun el esquema
    Se manejan errores si: no existe el centro"""
    sitio = Configuracion().sitio()
    centros = Centro().aprobados_paginado(1, sitio.paginas)
    centro2 = centros.next()
    pages = centros.pages
    per_page = centros.per_page
    if centros is None:
        response = {
            "message": "No existen centros",
        }
        return jsonify(response), 404
    centrosAPI = []
    for i in range(pages):
        centrosAPI.append(centros_schema.dump(centros.items))
        centros = centros.next()
    return jsonify({"centros": centrosAPI, "pages": pages, "per_page": per_page}, 200)


def index_all():
    """Retorna los centros activos y se convierte en json segun el esquema.
    Se manejan errores si: no existe el centro"""
    centros = Centro().aprobados()
    if centros is None:
        response = {
            "message": "No existen centros",
        }
        return jsonify(response), 404
    centrosAPI = []
    centrosAPI.append(centros_schema.dump(centros))
    return jsonify({"centros": centrosAPI}, 200)


def show_one(centro_id):
    """Busca un centro por id y lo retorna en formato JSON segun esquema.
    Se manejan errores si:no existe el centro o si existe un fallo en la bd"""
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
    result = centro_schema.dump(centro)
    return jsonify({"centro": result}, 200)


def new_centro():
    """Se parsea JSON de un centro y se convierte en un objeto para agregar a la bd.
    Se manejan errores si: falta algun campo, ya existe el centro o si existe un fallo en la bd"""
    json_data = request.get_json()
    if not json_data:
        response = {
            "message": "No se ingreso ningun dato",
        }
        return jsonify(response), 400
    try:
        """id_municipio = show_id_municipio(json_data["municipio"])"""
        data = centro_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 500

    (
        apertura,
        cierre,
        direccion,
        email,
        nombre,
        latitud,
        longitud,
        telefono,
        tipo_centro,
        web,
        id_municipio,
    ) = (
        data["apertura"],
        data["cierre"],
        data["direccion"],
        data["email"],
        data["nombre"],
        data["latitud"],
        data["longitud"],
        data["telefono"],
        data["tipo_centro"],
        data["web"],
        int(data["id_municipio"]),
    )

    try:
        centro = Centro().validate_centro_creation(
            nombre=nombre, direccion=direccion, municipio=id_municipio
        )
    except:
        response = {
            "message": "Fallo en servidor",
        }
        return jsonify(response), 500
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
            municipio=id_municipio,
            latitud=latitud,
            longitud=longitud,
        )
        db.session.add(centro)

        db.session.commit()
        result = centro_schema.dump(centro)
        return jsonify({"centro": result}, 201)
    else:
        response = {
            "message": "El centro ya existe",
        }
        return jsonify(response), 400

def tipos():
    try:
        tipo_centro = Centro().tipos()
    except:
        response = {
            "message": "Fallo en servidor",
        }
        return jsonify(response), 500

    tipoCentrosAPI = []

    tipoCentrosAPI.append(centros_schema.dump(tipo_centro))

    return jsonify({"centros": tipoCentrosAPI}, 200)
    
