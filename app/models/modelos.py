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

# Modelo configuracion
class Configuracion(db.Model):
    __tablename__ = "configuracion"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    email = db.Column(db.String(255))
    paginas = db.Column(db.Integer)
    activo = db.Column(db.Boolean, nullable=False)

    def create(conn, formulario):
        nuevo = Configuracion(
            email=formulario["email"],
            titulo=formulario["titulo"],
            descripcion=formulario["descripcion"],
            activo= eval(formulario["activo"]),
            paginas=formulario["paginado"]
        )
        db.session.add(nuevo)
        db.session.commit()

    def sitio(self, conn):
        sitio = Configuracion.query.all()
        return sitio


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
            username=formulario["user_name"],
            password=formulario["password"],
            activo= True,#formulario["activo"], 
            created_at=date.today(),
            first_name=formulario["first_name"],
            last_name=formulario["last_name"],
        )
        db.session.add(nuevo)
        db.session.commit()

    def all(conn):
        users = User.query.all()
        return users
    
    def __getitem__(self, email):
        return self.__dict__[email]

    def find_by_email_and_pass(self, conn, emailForm, passwordForm):
        user = User.query.filter(
            and_(User.email == emailForm, User.password == passwordForm)
        ).first()
        return user
    
    def find_by_username(self, conn, name):
        user = User.query.filter_by(User.username == name)
        return user
    '''
    def find_by_email(self, conn, email):
        user = self.query.filter_by(User.email == email)
        return user
    '''