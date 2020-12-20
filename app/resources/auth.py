from flask import redirect, render_template, request, url_for, abort, session, flash
from flask_bcrypt import Bcrypt
from app.helpers.auth import authenticated
from app.models.configuracion import Configuracion
from app.models.models import Permiso, User
from app.resources.forms import LoginForm


def login():
    """Loguea al usuario en el sistema, si la password es incorrecta devuelve error.
    La contraseña se encripta en la base de datos"""
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
    """Elimina datos de sesion del usuario logueado"""
    session.pop("user", None)
    session.pop("user_id", None)
    session.pop("permisos", None)
    session.clear()
    flash("La sesión se cerró correctamente.")
    return redirect(
        "https://admin-grupo13.proyecto2020.linti.unlp.edu.ar/iniciar_sesion"
    )
    # return redirect(
    #     "http://127.0.0.1:5000/iniciar_sesion"
    # )


def validate(form):
    """valida si el usuario existe, en la bd"""
    user = User().validate_user_creation(form["email"].data, form["username"].data)
    return user


def guardar_permisos(user_id):
    """busca los permisos del usuario por id y guardo sus permisos en la session"""
    permisos = []
    lista = Permiso().permisos_de_usuario(user_id)
    for permiso in lista:
        permisos.append(str(permiso.nombre))
    session["permisos"] = permisos
