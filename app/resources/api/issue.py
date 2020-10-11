from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import Rol


def index():
    conn = SQLAlchemy()
    # conn = connection()
    roles = Rol.all(conn)
    return jsonify(roles=roles)
