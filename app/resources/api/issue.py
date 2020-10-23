from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import Rol


def index():
    roles = Rol.all()
    return jsonify(roles=roles)
