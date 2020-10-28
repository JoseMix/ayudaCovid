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
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from config import config
from app import db
from app.resources import user
from app.resources import rol
from app.resources import permiso
from app.resources import configuracion
from app.resources import auth
from app.resources.api import issue as api_issue
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.resources.forms import RegistrationForm, LoginForm, FilterForm

# from app.db import connection
from app.models.configuracion import Configuracion, configuracion_initialize_db
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
    db = SQLAlchemy(app)
    initialize_db(app)
    configuracion_initialize_db(app)
    bcrypt = Bcrypt(app)

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
            user = User().find_by_email(form.email.data)
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                session["user"] = user["email"]
                session["user_id"] = user["id"]
                flash("Usuario logueado correctamente")
                # si se loguea correctamente lo nota con + funcionalidades
                return redirect(url_for("home"))
            else:
                flash("Usuario o Password incorrecto")
        sitio = Configuracion().sitio()
        return render_template("auth/login.html", form=form, sitio=sitio)

    # Rutas de Roles
    app.add_url_rule("/roles", "rol_index", rol.index)
    app.add_url_rule("/roles", "rol_create", rol.create, methods=["POST"])
    app.add_url_rule("/roles/nueva", "rol_new", rol.new)

    # Rutas de Permisos
    app.add_url_rule(
        "/permisos/<int:page>", "permiso_index", permiso.index, methods=["GET"]
    )

    app.add_url_rule("/permisos", "permiso_create", permiso.create, methods=["POST"])
    app.add_url_rule("/permisos/nueva", "permiso_new", permiso.new)

    # Rutas de Configuración
    app.add_url_rule(
        "/configuracion/editar", "configuracion_update", configuracion.update
    )
    app.add_url_rule(
        "/configuracion", "configuracion_edit", configuracion.edit, methods=["POST"]
    )
    app.add_url_rule("/configuracion", "configuracion_show", configuracion.show)

    # Rutas de Usuarios
    app.add_url_rule("/usuarios/<int:page>", "user_index", user.index, methods=["GET"])
    app.add_url_rule("/usuarios/show", "user_show", user.show)
    app.add_url_rule(
        "/usuarios/roles/<int:user_id>",
        "user_update_rol",
        user.update_rol,
        methods=["GET", "POST"],
    )
    # app.add_url_rule(
    #   "/usuarios/roles/update", "user_edit_rol", user.edit_rol,methods=["POST"]
    #  )
    # app.add_url_rule("/usuarios/eliminar<int:id>", 'update_user', controlador_principal.update_user, methods=['GET'])
    # app.add_url_rule("/usuarios/eliminar<int:id>", 'update_user', controlador_principal.update_user, methods=['GET'])
    app.add_url_rule(
        "/usuarios/eliminar/<int:user_id>",
        "user_eliminar",
        user.eliminar,
        methods=["GET"],
    )
    app.add_url_rule(
        "/usuarios/activar/<int:user_id>", "user_activar", user.activar, methods=["GET"]
    )

    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    # app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    # app.add_url_rule("/usuarios/modificar", "user_update", user.update)
    # app.add_url_rule("/usuarios", "user_", user., methods=["POST"])

    @app.route("/usuarios/modificar/<int:user_id>", methods=["GET", "POST"])
    def update_user(user_id):
        if not authenticated(session):
            abort(401)
        user = User.query.get_or_404(user_id)
        form = RegistrationForm(obj=user)
        if form.validate_on_submit():
            if not user.validate_user_update(
                form.email.data, form.username.data, user_id
            ):
                hashed_password = bcrypt.generate_password_hash(
                    form.password.data
                ).decode("utf-8")
                form.password.data = hashed_password
                form.populate_obj(user)
                user.set_update_time()
                db.session.merge(user)
                db.session.commit()
                return redirect(url_for("user_index", page=1))
            else:
                flash("El usuario o el email ya existe")
        sitio = Configuracion().sitio()
        return render_template("user/update.html", form=form, sitio=sitio)

    @app.route("/usuarios/nuevo", methods=["GET", "POST"])
    def register():
        if not authenticated(session):
            abort(401)
        form = RegistrationForm()
        if form.validate_on_submit():
            if not user.validate(form):
                hashed_password = bcrypt.generate_password_hash(
                    form.password.data
                ).decode("utf-8")
                form.password.data = hashed_password
                flash("Usuario creado con éxito")
                user.create(form)
                return redirect(url_for("user_index", page=1))
            else:
                flash("El usuario o el email ya existe")
        sitio = Configuracion().sitio()
        return render_template("user/new.html", form=form, sitio=sitio)

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        sitio = Configuracion().sitio()
        return render_template("home.html", sitio=sitio)

    # Ruta para el filtro de busqueda por nombre
    # app.add_url_rule("/usuarios/filter", "user_create", user.create, methods=["POST"])
    @app.route("/usuarios/filter", methods=["GET", "POST"])
    def filterByName():
        form = FilterForm()
        if request.method == "POST":
            sitio = Configuracion().sitio()
            index_pag = User().serchByName(form.nombre.data, 1, sitio.paginas)

            return render_template(
                "user/index.html", form=form, index_pag=index_pag, sitio=sitio
            )
        return render_template("user/filtroDeBusqueda.html", form=form)

    # Rutas de API-rest
    #    app.add_url_rule("/api/consultas", "api_issue_index", api_issue.index)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500 y 401

    # Retornar la instancia de app configurada
    return app
