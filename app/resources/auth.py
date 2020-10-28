from flask import redirect, render_template, request, url_for, abort, session, flash
from flask_bcrypt import Bcrypt

from app.models.configuracion import Configuracion
from app.models.models import User
from app.resources.forms import LoginForm


def login():
    form = LoginForm()
    bcrypt = Bcrypt()
    if form.validate_on_submit():
        user = User().find_by_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session["user"] = user["username"]
            session["user_id"] = user["id"]
            flash("Usuario logueado correctamente")
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
    session.clear()
    flash("La sesión se cerró correctamente.")
    return redirect(url_for("home"))


def validate(form):
    user = User().validate_user_creation(form["email"].data, form["username"].data)
    return user