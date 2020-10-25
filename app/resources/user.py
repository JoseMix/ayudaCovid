from flask import redirect, flash, render_template, request, url_for, session, abort
from app.models.models import User
from app.models.configuracion import Configuracion

from app.helpers.auth import authenticated

# Protected resources
def index():
    if not authenticated(session):
        abort(401)

    users = User().all()
    sitio = Configuracion().sitio()
    return render_template("user/index.html", users=users[0:sitio.paginas], sitio=sitio)


def show():
    if not authenticated(session):
        abort(401)
    user = User().find_by_id(session.get("user_id"))
    sitio = Configuracion().sitio()
    return render_template("user/show.html", user=user, sitio=sitio)


def new():
    if not authenticated(session):
        abort(401)
    sitio = Configuracion().sitio()
    return render_template("user/new.html", sitio=sitio)


def create(form):
    if not authenticated(session):
        abort(401)
    user = User()
    user.create(form)

def validate(form):
    user = User().validate_user_creation(form["email"].data, form["username"].data)
    return user


def eliminar(user_id):
    User().eliminar(id=user_id)
    users = User().all()
    sitio = Configuracion().sitio()
    flash("Usuario eliminado correctamente")
    return render_template("user/index.html", users=users[0:sitio.paginas], sitio=sitio)
    

def activar(user_id):
    User().activar(id=user_id)
    
    users = User().all()
    sitio = Configuracion().sitio()
    flash("Usuario activado correctamente")
    return render_template("user/index.html", users=users[0:sitio.paginas], sitio=sitio)
    

def update_rol(user_id):
    if not authenticated(session):
        abort(401)
    roles = User().mis_roles(user_id)
    otros_roles = User().otros_roles(user_id)
    sitio = Configuracion().sitio()
    return render_template("user/update_rol.html", roles=roles,otros_roles=otros_roles, sitio=sitio)


def edit_rol(form):
    return 1
