from os import path, environ
from flask import Flask, render_template, g, request, redirect, session, abort, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from config import config
from app import db
from app.resources import user, rol, permiso, configuracion
from app.resources import auth
from app.resources.api import issue as api_issue
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.models.modelos import initialize_db
from app.resources.forms import RegistrationForm, LoginForm
<<<<<<< HEAD
from app.models.modelos import User

=======
# from app.db import connection
from app.models.modelos import User
from app.helpers.auth import authenticated
>>>>>>> 9fd387b49e318a7aaf83aad74a8d90fc15da9d11

def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    app.config[
        "SQLALCHEMY_DATABASE_URI"
<<<<<<< HEAD
    ] = "mysql+pymysql://root:password@172.17.0.4/entrega1"
=======
    ] = "mysql+pymysql://root:@localhost/proyecto"
>>>>>>> 9fd387b49e318a7aaf83aad74a8d90fc15da9d11
    db = SQLAlchemy(app)
    """db.init_app(app)"""
    initialize_db(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)

    # Autenticación
    # app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    # app.add_url_rule("/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"])

    @app.route("/iniciar_sesion", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            if not (auth.authenticate(form)):
                flash("Usuario logueado correctamente")
                return redirect(url_for("home"))
        return render_template("auth/login.html", form=form)

    # Rutas de Roles
    app.add_url_rule("/roles", "rol_index", rol.index)
    app.add_url_rule("/roles", "rol_create", rol.create, methods=["POST"])
    app.add_url_rule("/roles/nueva", "rol_new", rol.new)

    # Rutas de Permisos
    app.add_url_rule("/permisos", "permiso_index", permiso.index)
    app.add_url_rule("/permisos", "permiso_create", permiso.create, methods=["POST"])
    app.add_url_rule("/permisos/nueva", "permiso_new", permiso.new)

    # Rutas de Configuración
    app.add_url_rule("/configuracion/nuevo", "configuracion_new", configuracion.new)
    app.add_url_rule(
        "/configuracion", "configuracion_create", configuracion.create, methods=["POST"]
    )
    # app.add_url_rule("/configuracion", "configuracion_show", configuracion.show)

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios/show", "user_show", user.show)

    # app.add_url_rule("/usuarios/eliminar<int:id>", 'update_user', controlador_principal.update_user, methods=['GET'])
    app.add_url_rule("/usuarios/eliminar<int:user_id>","user_eliminar", user.eliminar,methods=["GET"])

    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    # app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    # app.add_url_rule("/usuarios/modificar", "user_update", user.update)
    # app.add_url_rule("/usuarios", "user_", user., methods=["POST"])

<<<<<<< HEAD
    @app.route("/usuarios/<int:user_id>/modificar", methods=["GET", "POST"])
    def update_user(user_id):
        user = User.query.get_or_404(user_id)
        form = RegistrationForm(obj=user)
        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.merge(user)
            db.session.commit()
            # user.update(user, form)
            return redirect(url_for("user_index"))
        return render_template("user/update.html", form=form)
=======
    

>>>>>>> 9fd387b49e318a7aaf83aad74a8d90fc15da9d11

    @app.route("/usuarios/nuevo", methods=["GET", "POST"])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            if not user.validate(form):
                flash("Usuario creado con éxito")
                user.create(form)
                return redirect(url_for("home"))
            else:
                flash("El usuario o el email ya existe")
        return render_template("user/new.html", form=form, title="Actualizar usuario")

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        conn = SQLAlchemy()
        # conn = connection()
        us = User.all(conn)
        return render_template("home.html",us=us)

    # Rutas de API-rest
    #    app.add_url_rule("/api/consultas", "api_issue_index", api_issue.index)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500 y 401

    # Retornar la instancia de app configurada
    return app
