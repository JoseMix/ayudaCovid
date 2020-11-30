from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, text
from datetime import date


db = SQLAlchemy()


# Inicializo contexto
def initialize_db(app):
    app.app_context().push()
    db.init_app(app)
    db.create_all()


# Relaciones many to many
usuario_rol = db.Table(
    "usuario_rol",
    db.Column("rol_id", db.Integer, db.ForeignKey("rol.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

permiso_rol = db.Table(
    "permiso_rol",
    db.Column("rol_id", db.Integer, db.ForeignKey("rol.id"), primary_key=True),
    db.Column("permiso_id", db.Integer, db.ForeignKey("permiso.id"), primary_key=True),
)


# Modelo Rol
class Rol(db.Model):
    __tablename__ = "rol"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    permisos = db.relationship(
        "Permiso",
        secondary=permiso_rol,
        lazy="subquery",
        backref=db.backref("rol", lazy=True),
    )

    def all(self):
        roles = Rol.query.all()
        return roles

    def create(self, formulario):
        nuevo = Rol(nombre=formulario["rol"])
        db.session.add(nuevo)
        db.session.commit()

    def find_by_id(self, id):
        return Rol.query.filter(Rol.id == id).first()

    def is_admin(self, id_rol):
        return Rol.query.filter(and_(Rol.nombre == "administrador", Rol.id==id_rol) ).first()


# Modelo Permiso
class Permiso(db.Model):
    __tablename__ = "permiso"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    def __getitem__(self, nombre):
        return self.__dict__[nombre]

    def all(self):
        permisos = Permiso.query.all()
        return permisos

    def permiso_by_name(self, permiso):
        return Permiso.query.filter(Permiso.nombre == permiso).first()

#---------------------------------------------------------------------------
    def permisos_de_usuario(self, id):
        res = db.session.query(Permiso).join(User.roles).join(Rol.permisos).filter(User.id == id)
        return res

#---------------------------------------------------------------------------

    #page= página actual, per_page = elementos x página
    def all_paginado(self, page, per_page):
        return Permiso.query.order_by(Permiso.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def create(self, formulario):
        nuevo = Permiso(nombre=formulario["permiso"])
        db.session.add(nuevo)
        db.session.commit()


# Modelo Usuario
class User(db.Model):
    __tablename__ = "user"
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
        Rol,
        secondary=usuario_rol,
        lazy="subquery",
        backref=db.backref("user", lazy=True),
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

    def update(self, user):
        user.set_update_time()
        db.session.merge(user)
        db.session.commit()

    def all(self):
        users = User.query.all()
        return users

    # page= página actual, per_page = elementos x página
    def all_paginado(self,orden, page, per_page):
        return User.query.order_by(text(orden)).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def __getitem__(self, id):
        return self.__dict__[id]

    def set_update_time(self):
        self.updated_at = date.today()

    def find_by_email(self, emailForm):
        user = User.query.filter(
            and_(User.email == emailForm, User.activo == True)
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

    def eliminar(self, id):
        user = User().find_by_id(id)
        user.activo = False
        db.session.commit()
        return user

    def activar(self, id):
        user = User().find_by_id(id)
        user.activo = True
        db.session.commit()
        return user

    def search_by(self, username, estado,orden, page, per_page):
        if estado == '2':
            users = User().query.filter(User.username.ilike(f'%{username}%')).order_by(text(orden)).paginate(page=page, per_page=per_page, error_out=False)
        else:
            users = User().query.\
            filter(and_(User.username.ilike(f'%{username}%'), User.activo == estado)).order_by(text(orden)).\
            paginate(page=page, per_page=per_page, error_out=False)
        
        return users

    #--------------------- Roles de usuario -----------------
    #recibe el id del usuario y el rol-string-
    def tiene_rol(self, id, rol):
        return db.session.query(User).join(Rol, User.roles).\
        filter(and_(User.id== id, Rol.nombre == rol)).first()
    #---------------------------------------------------------

    #recibe un usuario y un rol para desasignar
    def delete_rol(self, rol, user):
        user.roles.remove(rol)
        db.session.commit()

    #recibe un usuario y un rol para asignar
    def add_rol(self, rol, user):
        user.roles.append(rol)
        db.session.commit()

    #verifica que exista otro administrador
    def unico_admin(self, id_rol, id_user):
        return db.session.query(Rol).join(User.roles).filter(and_(Rol.id==id_rol, User.id!=id_user)).all()


