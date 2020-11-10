from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.centro import Centro, centro_schema, centros_schema


def index():
    centros = Centro().all()
    result = centros_schema.dump(centros)
    return jsonify(result)


def showOne(centro_id):
    centro = Centro().showOne(centro_id)
    result = centro_schema.dump(centro)
    return jsonify(result)


"""
def create(form):
    #falta"""
