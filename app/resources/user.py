from flask import redirect, flash, render_template, request, url_for, session, abort
from app.models.models import User
from app.models.configuracion import Configuracion
from app.resources.forms import RegistrationForm
from app.helpers.auth import authenticated

# Protected resources
def index(page=1):
    if not authenticated(session):
        abort(401)
    form = RegistrationForm()
    
    sitio = Configuracion().sitio()
    index_pag = User().all_paginado(page, sitio.paginas)
    return render_template("user/index.html", form=form, index_pag=index_pag, sitio=sitio)


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
    sitio = Configuracion().sitio()
    index_pag = User().all_paginado(1, sitio.paginas)
    flash("Usuario eliminado correctamente")
    form = RegistrationForm()
    return render_template("user/index.html",form=form, index_pag=index_pag, sitio=sitio)
    

def activar(user_id):
    User().activar(id=user_id)
    sitio = Configuracion().sitio()
    index_pag = User().all_paginado(1, sitio.paginas)
    flash("Usuario activado correctamente")
    form = RegistrationForm()
    return render_template("user/index.html",form=form, index_pag=index_pag, sitio=sitio)
    

def update_rol(user_id):
    if not authenticated(session):
        abort(401)
    roles = User().mis_roles(user_id)
    otros_roles = User().otros_roles(user_id)

    print('mis roles:', roles)
    print('mis no roles:', otros_roles)

    sitio = Configuracion().sitio()
    return render_template("user/update_rol.html",user_id=user_id, roles=roles, otros_roles=otros_roles, sitio=sitio)


def edit_roles(form):
    user = User().find_by_id(form.id)
    print(user)
    print(form.roles)
    print('aca esta por entrar al')
    User.update_roles(form, user)
    print('aca llegaaaaaaaaaaaaaaaaaaaaaaaa')
    update_rol(user_id=form.id)
