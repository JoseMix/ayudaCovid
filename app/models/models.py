from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, text
from datetime import date


db = SQLAlchemy()


def initialize_db(app):
    """ Inicializo contexto"""
    app.app_context().push()
    db.init_app(app)
    db.create_all()


"""esquema de relaciones many to many usuario-rol"""
usuario_rol = db.Table(
    "usuario_rol",
    db.Column("rol_id", db.Integer, db.ForeignKey("rol.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)
"""esquema de relaciones many to many permiso-rol"""
permiso_rol = db.Table(
    "permiso_rol",
    db.Column("rol_id", db.Integer, db.ForeignKey("rol.id"), primary_key=True),
    db.Column("permiso_id", db.Integer, db.ForeignKey("permiso.id"), primary_key=True),
)


class Rol(db.Model):
    """ Modelo Rol de usuarios"""

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
        """devuelve roles de bd"""
        roles = Rol.query.all()
        return roles

    def create(self, formulario):
        """carga un nuevo rol en la bd"""
        nuevo = Rol(nombre=formulario["rol"])
        db.session.add(nuevo)
        db.session.commit()

    def find_by_id(self, id):
        """busca un rol por su id"""
        return Rol.query.filter(Rol.id == id).first()

    def is_admin(self, id_rol):
        """verifica si el id pertenece a un administrador"""
        return Rol.query.filter(
            and_(Rol.nombre == "administrador", Rol.id == id_rol)
        ).first()


class Permiso(db.Model):
    """ Modelo permisos de rol"""

    __tablename__ = "permiso"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    def __getitem__(self, nombre):
        return self.__dict__[nombre]

    def all(self):
        """devuelve los permisos de la bd"""
        permisos = Permiso.query.all()
        return permisos

    def permiso_by_name(self, permiso):
        """busca un permiso por nombre"""
        return Permiso.query.filter(Permiso.nombre == permiso).first()

    def permisos_de_usuario(self, id):
        """devuelve los permisos de un usuario"""
        res = (
            db.session.query(Permiso)
            .join(User.roles)
            .join(Rol.permisos)
            .filter(User.id == id)
        )
        return res

    def all_paginado(self, page, per_page):
        """devuelve permisos paginados por page= página actual, per_page = elementos x página"""
        return Permiso.query.order_by(Permiso.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def create(self, formulario):
        """crea un nuevo permiso"""
        nuevo = Permiso(nombre=formulario["permiso"])
        db.session.add(nuevo)
        db.session.commit()


# Modelo Usuario
class User(db.Model):
    """ Modelo Usuario"""

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
        """carga un nuevo usuario en la bd"""
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
        """setea la hora de actualizacion en el registro modificado"""
        user.updated_at = date.today()
        # user.set_update_time() SI FUNCIONA EL UPDATE BORRAR ESTA LINEA!!!!!
        db.session.merge(user)
        db.session.commit()

    def all(self):
        """devuelve todos los usuarios de la bd"""
        users = User.query.all()
        return users

    def all_paginado(self, orden, page, per_page):
        """devuelve los usuarios ordenados por criterio y paginados"""
        return User.query.order_by(text(orden)).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def __getitem__(self, id):
        return self.__dict__[id]

    """ def set_update_time(self): SI FUNCIONA EL UPDATE BORRAR ESTO************
        self.updated_at = date.today()"""

    def find_by_email(self, emailForm):
        """busca usuario por email"""
        user = User.query.filter(
            and_(User.email == emailForm, User.activo == True)
        ).first()
        return user

    def find_by_username(self, name):
        """busca usuario por username"""
        user = User.query.filter_by(User.username == name)
        return user

    def find_by_id(self, id):
        """busca usuario por id"""
        user = User.query.filter(User.id == id).first()
        return user

    def validate_user_creation(self, emailForm, usernameForm):
        """valida que el usuario no exista"""
        user = User.query.filter(
            or_(User.email == emailForm, User.username == usernameForm)
        ).first()
        return user

    def validate_user_update(self, emailForm, usernameForm, id):
        """valida que el usuario que se quiere modificar, no tome datos existentes"""
        user = User.query.filter(
            or_(User.email == emailForm, User.username == usernameForm),
            and_(User.id != id),
        ).first()
        return user

    def eliminar(self, id):
        """elimina usuario de la bd"""
        user = User().find_by_id(id)
        user.activo = False
        db.session.commit()
        return user

    def activar(self, id):
        """activa usuario"""
        user = User().find_by_id(id)
        user.activo = True
        db.session.commit()
        return user

    def search_by(self, username, estado, orden, page, per_page):
        """busca un usuario paginado"""
        if estado == "2":
            users = (
                User()
                .query.filter(User.username.ilike(f"%{username}%"))
                .order_by(text(orden))
                .paginate(page=page, per_page=per_page, error_out=False)
            )
        else:
            users = (
                User()
                .query.filter(
                    and_(User.username.ilike(f"%{username}%"), User.activo == estado)
                )
                .order_by(text(orden))
                .paginate(page=page, per_page=per_page, error_out=False)
            )

        return users

    def tiene_rol(self, id, rol):
        """retorna los roles de un usuario"""
        return (
            db.session.query(User)
            .join(Rol, User.roles)
            .filter(and_(User.id == id, Rol.nombre == rol))
            .first()
        )

    def delete_rol(self, rol, user):
        """desasigna un rol a un usuario"""
        user.roles.remove(rol)
        db.session.commit()

    def add_rol(self, rol, user):
        """recibe un usuario y un rol para asignar"""
        user.roles.append(rol)
        db.session.commit()

    def unico_admin(self, id_rol, id_user):
        """ verifica que exista otro administrador"""
        return (
            db.session.query(Rol)
            .join(User.roles)
            .filter(and_(Rol.id == id_rol, User.id != id_user))
            .all()
        )
