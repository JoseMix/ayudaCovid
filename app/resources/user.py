from flask import redirect, render_template, request, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy

# from app.db import connection
from app.models.modelos import User, Rol, Configuracion, Permiso
from app.helpers.auth import authenticated

# Protected resources
def index():
    if not authenticated(session):
        abort(401)
    conn = SQLAlchemy()
    users = User.all(conn)
    sitio = Configuracion.sitio()
    return render_template("user/index.html", users=users, sitio=sitio)


def show():
    if not authenticated(session):
        abort(401)
    user = User().find_by_id(1)
    print(user)
    sitio = Configuracion.sitio()
    return render_template("user/show.html", user=user, sitio=sitio)


def new():
    if not authenticated(session):
        abort(401)
    sitio = Configuracion.sitio()
    return render_template("user/new.html", sitio=sitio)


def create(form):
    conn = SQLAlchemy()
    # conn = connection()
    user = User()
    user.create(conn, form)
    # Crear y redirigir logueado
    return redirect(url_for("login"))


def validate(form):
    user = User().validate_user_creation(form["email"].data, form["username"].data)
    return user

def eliminar(user_id):
    User().eliminar(id=user_id)
    return render_template("user/eliminar.html")

def activar(user_id):
    User().activar(id=user_id)
    return render_template("user/activar.html")
    
def update_rol(user_id):
   
    roles = User().mis_roles(user_id)

    sitio = Configuracion.sitio()
    print(roles)
    return render_template("user/update_rol.html", roles=roles, sitio=sitio)

def edit_rol(form):
    return 1  
