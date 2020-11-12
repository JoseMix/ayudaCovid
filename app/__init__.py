from os import path, environ
from flask import (
    Flask,
    render_template,
    g,
    request,
    redirect,
    session,
    abort,
    url_for,
    flash,
    abort,
)
import requests
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_marshmallow import Marshmallow
from app.resources import user, configuracion, auth, centro, turnos
from app.resources.api import centros

# from app.resources.api import centro
from config import config
from app import db
from app.resources import user, configuracion, auth, centro

# from app.helpers import handler
from app.helpers import auth as helper_auth
from app.resources.forms import RegistrationForm, LoginForm, FilterForm, CrearCentroForm

# from app.db import connection
from app.models.configuracion import Configuracion, configuracion_initialize_db
from app.models.centro import Bloque, Centro, Turnos, centro_turnos_initialize_db
from app.models.models import Rol, Permiso, User, initialize_db
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
    ] = "mysql+pymysql://root:password@172.17.0.4/grupo13"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)
    ma = Marshmallow(app)
    initialize_db(app)
    configuracion_initialize_db(app)
    centro_turnos_initialize_db(app)
    # bcrypt = Bcrypt(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)

    # Autenticación
    app.add_url_rule(
        "/iniciar_sesion", "auth_login", auth.login, methods=["GET", "POST"]
    )
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)

    # Rutas de Configuración
    app.add_url_rule(
        "/configuracion/editar", "configuracion_update", configuracion.update
    )
    app.add_url_rule(
        "/configuracion", "configuracion_edit", configuracion.edit, methods=["POST"]
    )
    app.add_url_rule("/configuracion", "configuracion_show", configuracion.show)

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index, methods=["GET", "POST"])
    app.add_url_rule("/usuarios/show", "user_show", user.show)
    app.add_url_rule(
        "/usuarios/roles/<int:user_id>",
        "user_update_rol",
        user.update_rol,
        methods=["GET", "POST"],
    )

    app.add_url_rule(
        "/usuarios/eliminar/<int:user_id>,<int:page>",
        "user_eliminar",
        user.eliminar,
        methods=["GET"],
    )
    app.add_url_rule(
        "/usuarios/activar/<int:user_id>,<int:page>",
        "user_activar",
        user.activar,
        methods=["GET"],
    )
    app.add_url_rule(
        "/usuarios/nuevo", "user_register", user.register, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/usuarios/modificar/<int:user_id>",
        "user_update",
        user.update,
        methods=["GET", "POST"],
    )

    # Rutas de Centros
    app.add_url_rule(
        "/centro/listado/<int:page>", "centro_index", centro.index, methods=["GET"]
    )
    app.add_url_rule("/centro/show", "centro_show", centro.show, methods=["GET"])
    app.add_url_rule(
        "/centro/nuevo", "centro_register", centro.register, methods=["GET", "POST"]
    )
    # app.add_url_rule("/centro/show_municipio", "centro_show_municipio", centro.show_municipio)

    # Rutas de Turnos
    app.add_url_rule("/turnos", "turnos_index", turnos.index, methods=["GET", "POST"])
    app.add_url_rule("/turnos/nuevo", "turnos_new", turnos.new, methods=["GET"])
    app.add_url_rule("/turnos/nuevo", "turnos_create", turnos.create, methods=["POST"])
    app.add_url_rule(
        "/turnos/eliminar/", "turnos_eliminar", turnos.eliminar, methods=["GET"]
    )

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        sitio = Configuracion().sitio()
        return render_template("home.html", sitio=sitio)

    # Rutas de API-rest
    app.add_url_rule("/api/centros", "api_centros_index", centros.index)
    app.add_url_rule(
        "/api/centros",
        "api_centros_new_centro",
        centros.new_centro,
        methods=["POST"],
    )
    app.add_url_rule(
        "/api/centros/<int:centro_id>", "api_centros_show_one", centros.show_one
    )

    # Handlers
    # app.register_error_handler(404, handler.not_found_error)
    # app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500 y 401

    # Retornar la instancia de app configurada
    return app
