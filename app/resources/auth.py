from flask import redirect, render_template, request, url_for, abort, session, flash
from flask_bcrypt import Bcrypt

# from app.db import connection
from app.models.configuracion import Configuracion
#from app.models.permiso import Permiso
#from app.models.rol_permiso import Rol
from app.models.models import User


'''def authenticate(form, bcrypt):
    print('entra al autenticatee AUTHHHH')
    user = User().find_by_email(form.email.data)
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        session["user"] = user["email"]
        session["user_id"] = user["id"]
        flash("Usuario logueado correctamente")
        #si se loguea correctamente lo nota con + funcionalidades
        return redirect(url_for("home"))
    else:
        flash("Usuario o Password")
        sitio = Configuracion().sitio()
        return render_template("auth/login.html", form=form, sitio=sitio)

'''

def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("home"))


def validate(form):
    user = User().validate_user_creation(
         form["email"].data, form["username"].data
    )
    return user