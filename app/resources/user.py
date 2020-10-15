from flask import redirect, render_template, request, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import User
from app.helpers.auth import authenticated

# Protected resources
def index():
    if not authenticated(session):
        abort(401)
    conn = SQLAlchemy()
    # conn = connection()
    users = User.all(conn)

    return render_template("user/index.html", users=users)

'''
def show():
    if not authenticated(session):
        abort(401)
    conn = SQLAlchemy()
    user = User.find_by_email(conn, session.get("user"))
   
    return render_template("user/show.html", user=user.get(1))    
 '''
 
def new():
    if not authenticated(session):
        abort(401)

    return render_template("user/new.html")


def create():
    if not authenticated(session):
        abort(401)
    conn = SQLAlchemy()
    # conn = connection()
    User.create(conn, request.form)
    return redirect(url_for("user_index"))
