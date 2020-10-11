from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from datetime import date

db = SQLAlchemy()


# Inicializo contexto
def initialize_db(app):
    app.app_context().push()
    db.init_app(app)
    db.create_all()


# Relaciones many to many
permiso_rol = db.Table(
    "permiso_rol",
    db.Column("roles_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "permisos_id", db.Integer, db.ForeignKey("permisos.id"), primary_key=True
    ),
)

usuario_rol = db.Table(
    "usuario_rol",
    db.Column("roles_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column("users_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)


# Modelo Rol
class Rol(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    permisos = db.relationship(
        "Rol",
        secondary=permiso_rol,
        lazy="subquery",
        backref=db.backref("roles", lazy=True),
    )

    def all(conn):
        roles = Rol.query.all()
        return roles

    def create(conn, formulario):
        nuevo = Rol(nombre=formulario["rol"])
        db.session.add(nuevo)
        db.session.commit()


# Modelo Permiso
class Permiso(db.Model):
    __tablename__ = "permisos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    def all(conn):
        permisos = Permiso.query.all()
        return permisos

    def create(conn, formulario):
        nuevo = Permiso(nombre=formulario["permiso"])
        db.session.add(nuevo)
        db.session.commit()


# Modelo Usuario
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    updated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    roles = db.relationship(
        "Rol",
        secondary=usuario_rol,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )

    def create(conn, formulario):
        nuevo = User(
            email=formulario["email"],
            username=formulario["username"],
            password=formulario["password"],
            activo=formulario["activo"],
            created_at=date.today(),
            first_name=formulario["first_name"],
            last_name=formulario["last_name"],
        )
        db.session.add(nuevo)
        db.session.commit()

    def all(conn):
        users = User.query.all()
        return users
