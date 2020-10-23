from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
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

    def create(formulario):
        nuevo = Configuracion(
            email=formulario["email"],
            titulo=formulario["titulo"],
            descripcion=formulario["descripcion"],
            activo=eval(formulario["activo"]),
            paginas=formulario["paginado"],
        )
        db.session.add(nuevo)
        db.session.commit()

    def sitio():
        s = Configuracion.query.all()  # no me funciono el limit(1)
        sitio = s[0]
        return sitio

    def edit(formulario):
        sitio = Configuracion.sitio()
        sitio.email = formulario["email"]
        sitio.titulo = formulario["titulo"]
        sitio.descripcion = formulario["descripcion"]
        sitio.activo = eval(formulario["activo"])
        sitio.paginas = formulario["paginas"]
        db.session.commit()


# Modelo Rol
class Rol(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    permisos = db.relationship(
        "Permiso",
        secondary=permiso_rol,
        lazy="subquery",
        backref=db.backref("roles", lazy=True),
    )

    def all():
        roles = Rol.query.all()
        return roles

    def create(formulario):
        nuevo = Rol(nombre=formulario["rol"])
        db.session.add(nuevo)
        db.session.commit()


# Modelo Permiso
class Permiso(db.Model):
    __tablename__ = "permisos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    def all():
        permisos = Permiso.query.all()
        return permisos

    def create(formulario):
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

    def create(self, formulario):
        nuevo = User(
            email=formulario["email"].data,
            username=formulario["username"].data,
            password=formulario["password"].data,
            activo=True,  # formulario["activo"],
            created_at=date.today(),
            first_name=formulario["first_name"].data,
            last_name=formulario["last_name"].data,
        )
        db.session.add(nuevo)
        db.session.commit()

    def all():
        users = User.query.all()
        return users

    def __getitem__(self, id):
        return self.__dict__[id]

    def __getitem__(self, email):
        return self.__dict__[email]

    def __getitem__(self, password):
        return self.__dict__[password]

    def set_update_time(self):
        self.updated_at = date.today()

    def find_by_email_and_pass(self, emailForm, usernameForm):
        user = User.query.filter(
            and_(User.email == emailForm, User.password == usernameForm)
        ).first()
        return user

    def find_by_username(self, name):
        user = User.query.filter_by(User.username == name)
        return user

    def find_by_id(self, id):
        user = User.query.filter(User.id == id).first()
        return user

    def validate_user_creation(self, emailForm, usernameForm):
        user = User.query.filter(
            or_(User.email == emailForm, User.username == usernameForm)
        ).first()
        return user

    def validate_user_update(self, emailForm, usernameForm, id):
        user = User.query.filter(
            or_(User.email == emailForm, User.username == usernameForm),
            and_(User.id != id),
        ).first()
        return user

    def mis_roles(self, id):
        roles = db.session.query(Rol).join(Rol, User.roles).filter(User.id == id)
        return roles
    
    def mis_permisos(self, id):
        permisos = db.session.query(Permiso).join(Permiso, Rol.permisos)\
            .join(Rol, User.roles).filter(User.id == id)
        return permisos

    def roles_usuarios():
        roles_y_usuarios = db.session.query(Rol, User).join(Rol, User.roles).all()
        return roles_y_usuarios
    
    def otros_roles(self, id):
        roles = db.session.query(Rol).join(Rol, User.roles).filter(User.id != id)
        return roles
    
    ''' roles = db.session.query(Rol).join(Rol, User.roles).filter(~Rol.id.in_(User().mis_roles(id))) tiro error. ver '''
            
    def eliminar(self,id):
            user = User().find_by_id(id)
            user.activo = False
            db.session.commit()
            return user

    def activar(self,id):
            user = User().find_by_id(id)
            user.activo = True
            db.session.commit()
            return user 
                   
    def serchByName(self,name):
        users = User().query.filter(User.first_name.ilike(f'%{name}%')).all()
        return users  
    
  
