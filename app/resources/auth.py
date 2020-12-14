from flask import redirect, render_template, request, url_for, abort, session, flash
from flask_bcrypt import Bcrypt
from app.helpers.auth import authenticated
from app.models.configuracion import Configuracion
from app.models.models import Permiso, User
from app.resources.forms import LoginForm

def login():
    if authenticated(session):
        return redirect(url_for("home"))
    form = LoginForm()
    bcrypt = Bcrypt()
    if form.validate_on_submit():
        user = User().find_by_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session["user"] = user["username"]
            session["user_id"] = user["id"]
            flash("Usuario logueado correctamente")
            guardar_permisos(user.id)
            return redirect(url_for("home"))
        else:
            flash("Usuario o Password incorrecto")
            return render_template("auth/login.html", form=form)
    else:
        return render_template("auth/login.html", form=form)


def logout():
    # del session['user']
    session.pop("user", None)
    session.pop("user_id", None)
    session.pop("permisos", None)
    session.clear()
    flash("La sesión se cerró correctamente.")
    return redirect('https://admin-grupo13.proyecto2020.linti.unlp.edu.ar/iniciar_sesion')


def validate(form):
    user = User().validate_user_creation(form["email"].data, form["username"].data)
    return user


def guardar_permisos(user_id):
    #busca los permisos del usuario con id==user_id
    permisos = []
    lista = Permiso().permisos_de_usuario(user_id)
    #me quedo con los nombres(string) de los permisos y los guardo en la sesion
    for permiso in lista:
        permisos.append(str(permiso.nombre))
    session['permisos']= permisos


