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
# from app.db import connection
from app.models.modelos import User
from app.helpers.auth import authenticated

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
    ] = "mysql+pymysql://root:@localhost/proyecto"
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
    # app.add_url_rule("/usuarios/show", "user_show", user.show)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    # app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    # app.add_url_rule("/usuarios/modificar", "user_update", user.update)
    # app.add_url_rule("/usuarios", "user_", user., methods=["POST"])

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
        return render_template("user/new.html", form=form)

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
