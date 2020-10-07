from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.issue import Issue


def index():
    conn = SQLAlchemy()
    # conn = connection()
    issues = Issue.all(conn)
    return jsonify(issues=issues)
