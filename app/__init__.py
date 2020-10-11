from os import path, environ
from flask import Flask, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from config import config
from app import db
from app.resources import user
from app.resources import auth
from app.resources.api import issue as api_issue
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.models.modelos import initialize_db


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
>>>>>>> development
    db = SQLAlchemy(app)
    """db.init_app(app)"""
    initialize_db(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )
    """
    # Rutas de Consultas
    app.add_url_rule("/consultas", "issue_index", issue.index)
    app.add_url_rule("/consultas", "issue_create", issue.create, methods=["POST"])
    app.add_url_rule("/consultas/nueva", "issue_new", issue.new)
    """
    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
#   app.add_url_rule("/usuarios/modificar", "user_update", user.update)
#   app.add_url_rule("/usuarios", "user_", user., methods=["POST"])

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        return render_template("home.html")

    # Rutas de API-rest
    app.add_url_rule("/api/consultas", "api_issue_index", api_issue.index)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500 y 401

    # Retornar la instancia de app configurada
    return app
