from flask import redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import Permiso

"""
# Public resources
def index():
    conn = SQLAlchemy()
    # conn = connection()
    issues = Issue.all(conn)

    return render_template("issue/index.html", issues=issues)


def new():
    return render_template("issue/new.html")


def create():
    conn = SQLAlchemy()
    # conn = connection()
    Issue.create(conn, request.form)

    return redirect(url_for("issue_index"))
"""