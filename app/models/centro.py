from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, func
from operator import and_
from marshmallow import Schema, fields, ValidationError
from sqlalchemy.dialects import mysql

db = SQLAlchemy()


def centro_turnos_initialize_db(app):
    """ Inicializo contexto"""
    app.app_context().push()
    db.init_app(app)
    db.create_all()


class Turnos(db.Model):
    """ Modelo Turnos de centros"""

    __tablename__ = "turnos"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255))
    apellido = db.Column(db.String(255))
    telefono = db.Column(db.String(20))
    dia = db.Column(db.DateTime, nullable=False)
    estado = db.Column(
        db.Enum("VIGENTE", "CANCELADO"), nullable=False, default="VIGENTE"
    )
    turno_id = db.Column(db.Integer, db.ForeignKey("bloque.id"), nullable=False)
    centro_id = db.Column(db.Integer, db.ForeignKey("centro.id"), nullable=False)

    def create(self, form):
        """Crea un turno y lo añade a la bd"""
        turno = Turnos(
            email=form["email"],
            dia=form["dia"],
            turno_id=form["bloque"],
            centro_id=form["centro_id"],
        )
        db.session.add(turno)
        db.session.commit()

    def eliminar(self, id):
        """ Baja lógica de turno"""
        turno = Turnos().find_by_id(id)
        turno.estado = "CANCELADO"
        db.session.commit()

    def find_by_id(self, id):
        """busca turno por id"""
        return Turnos.query.filter(Turnos.id == id).first()

    def turno_centro(self, centro_id):
        """busca los turnos de un centro"""
        return Turnos.query.filter(Turnos.centro_id == centro_id).all()

    def find_by(self, dia, bloque, centro_id):
        """Valida si el turno esta repetido """
        return Turnos.query.filter(
            and_(Turnos.centro_id == centro_id, Turnos.turno_id == bloque),
            Turnos.dia == dia,
            Turnos.estado == "VIGENTE",
        ).first()

    def turnos_by_email(self, email, centro_id, page, per_page):
        """  busca turnos por email """
        if email == "todos":
            return (
                Turnos.query.filter(Turnos.centro_id == centro_id)
                .order_by(Turnos.dia.asc(), Turnos.turno_id.asc())
                .paginate(page=page, per_page=per_page, error_out=False)
            )
        else:
            return (
                Turnos.query.filter(
                    and_(Turnos.email == email, Turnos.centro_id == centro_id)
                )
                .order_by(Turnos.dia.asc(), Turnos.turno_id.asc())
                .paginate(page=page, per_page=per_page, error_out=False)
            )

    def turno_centro_fecha(self, centro_id, fecha):
        """busca los turnos para una fecha"""
        return Turnos.query.filter(
            and_(Turnos.dia == fecha, Turnos.centro_id == centro_id)
        ).all()

    def validar_turno_existente(self, id_bloque, id_centro, fecha):
        """verifica si el turno ya existe"""
        return Turnos.query.filter(
            and_(
                and_(Turnos.turno_id == id_bloque, Turnos.centro_id == id_centro),
                Turnos.dia == fecha,
            )
        ).first()

    def top(self, cantidad):
        return (
            db.session.query(Centro.id, func.count(Centro.municipio).label("cantidad"))
            .join(Centro.turnos)
            .group_by(Centro.municipio)
            .limit(cantidad)
            .all()
        )


class TurnoSchema(Schema):
    """ Esquema de Turnos de centros para api marshmallow"""

    id = fields.Int()
    centro_id = fields.Str()
    email = fields.Str()
    nombre = fields.Str()
    apellido = fields.Str()
    telefono = fields.Str()
    hora_inicio = fields.DateTime(format="%H:%M")
    hora_fin = fields.DateTime(format="%H:%M")
    fecha = fields.Date(format="%d-%m-%Y")
    cantidad = fields.Int()

    class Meta:
        """ campos del esquema de turnos para api marshmallow ordenados"""

        fields = (
            "id",
            "centro_id",
            "email",
            "nombre",
            "apellido",
            "telefono",
            "fecha",
            "hora_inicio",
            "hora_fin",
            "cantidad",
        )
        ordered = True


turno_schema = TurnoSchema()
turnos_schema = TurnoSchema(many=True)


# Modelo Bloque de turnos
class Bloque(db.Model):
    """ Modelo bloques"""

    __tablename__ = "bloque"
    id = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    turnos = db.relationship("Turnos", backref="bloque", lazy=True)

    def all(self):
        """retorna todos los bloques"""
        return Bloque.query.all()

    def find_by_id(self, id):
        """busca un bloque por id de bloque"""
        return Bloque.query.filter_by(id=id).first()

    def find_by_hora_inicio(self, hora):
        """busca el id de bloque por su hora de inicio"""
        bloque = Bloque.query.filter_by(hora_inicio=hora).first()
        return bloque

    def bloques_ocupados(self, centro_id, fecha):
        """devuelve los bloques ocupados en un centro en una fecha"""
        return (
            db.session.query(Bloque)
            .join(Bloque.turnos)
            .filter(
                and_(
                    and_(Turnos.dia == fecha, Turnos.centro_id == centro_id),
                    and_(Turnos.turno_id == Bloque.id, Turnos.estado != "CANCELADO"),
                )
            )
            .all()
        )


class Centro(db.Model):
    """ Modelo centro"""

    __tablename__ = "centro"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    apertura = db.Column(db.Time, nullable=False)
    cierre = db.Column(db.Time, nullable=False)
    tipo_centro = db.Column(db.Enum("COMIDA", "ROPA", "PLASMA"), nullable=False)
    municipio = db.Column(db.Integer, nullable=False)
    web = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    estado = db.Column(
        db.Enum("RECHAZADO", "ACEPTADO", "PENDIENTE"),
        nullable=False,
        default="PENDIENTE",
    )
    publicado = db.Column(db.Boolean, nullable=False, default=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    protocolo = db.Column(db.String(255), nullable=True)
    latitud = db.Column(db.Float, nullable=True)
    longitud = db.Column(db.Float, nullable=True)
    turnos = db.relationship("Turnos", backref="centro", lazy=True)

    def search_by(self, name, estado, orden, page, per_page):
        """busca un centro en cualquier estado"""
        if estado == "3":
            centro = (
                Centro()
                .query.filter(Centro.nombre.ilike(f"%{name}%"))
                .order_by(text(orden))
                .paginate(page=page, per_page=per_page, error_out=False)
            )
        else:
            """si no se buscó por nombre, busca solo por estado"""
            if name == "":
                centro = (
                    Centro()
                    .query.filter(Centro.estado == estado)
                    .order_by(text(orden))
                    .paginate(page=page, per_page=per_page, error_out=False)
                )
            else:
                """si se buscó por nombre y por estado"""
                centro = (
                    Centro()
                    .query.filter(
                        and_(Centro.nombre.ilike(f"%{name}%"), Centro.estado == estado)
                    )
                    .order_by(text(orden))
                    .paginate(page=page, per_page=per_page, error_out=False)
                )
        return centro

    def tipos(self):
        return (
            db.session.query(
                Centro.tipo_centro, func.count(Centro.tipo_centro).label("cantidad")
            )
            .group_by(Centro.tipo_centro)
            .all()
        )

    def turnos_por_tipo(self, fecha_inicio, fecha_fin):
        return (
            db.session.query(
                Centro.tipo_centro, func.count(Centro.tipo_centro).label("cantidad")
            ).filter(Turnos.dia.between(fecha_inicio, fecha_fin))
            .join(Turnos.centro)
            .group_by(Centro.tipo_centro)
            .all()
        )

    def all(self):
        """devuelve todos los centros"""
        centros = Centro.query.all()
        return centros

    def aprobados_paginado(self, page, per_page):
        """devuelve todos los centros aprobados y paginado"""
        centros = Centro.query.filter(
            and_(Centro.estado == "Aceptado", Centro.activo == True)
        ).paginate(page=page, per_page=per_page, error_out=False)
        return centros

    def aprobados(self):
        """devuelve todos los centros aprobados sin paginado"""
        centros = Centro.query.filter(
            and_(
                and_(Centro.estado == "Aceptado", Centro.activo == True),
                Centro.publicado == True,
            )
        ).all()
        return centros

    def find_by_id(self, id):
        """busca centor por id"""
        centro = Centro.query.filter(Centro.id == id).first()
        return centro

    def all_paginado(self, orden, page, per_page):
        """devuelve los centros ordenados con los siguientes criterios: page= página actual, per_page = elementos x página"""
        return Centro.query.order_by(text(orden)).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def create(self, formulario, nameProtocolo):
        """Crea un centro y lo añade a la bd"""
        nuevo = Centro(
            nombre=formulario["nombre"].data,
            direccion=formulario["direccion"].data,
            telefono=formulario["telefono"].data,
            apertura=formulario["apertura"].data,
            cierre=formulario["cierre"].data,
            tipo_centro=formulario["tipo_centro"].data,
            municipio=formulario["municipio"].data,
            web=formulario["web"].data,
            email=formulario["email"].data,
            publicado=False,
            activo=True,
            protocolo=nameProtocolo,
            latitud=formulario["lat"].data,
            longitud=formulario["lng"].data,
        )
        db.session.add(nuevo)
        db.session.commit()

    # actualiza centro con datos del form
    def update(self, formulario, centro):
        """actualiza un centro en la bd"""
        centro.nombre = formulario["nombre"].data
        centro.direccion = formulario["direccion"].data
        centro.telefono = formulario["telefono"].data
        centro.apertura = formulario["apertura"].data
        centro.cierre = formulario["cierre"].data
        centro.tipo_centro = formulario["tipo_centro"].data
        centro.municipio = formulario["municipio"].data
        centro.web = formulario["web"].data
        centro.email = formulario["email"].data
        centro.latitud = formulario["lat"].data
        centro.longitud = formulario["lng"].data

        db.session.merge(centro)
        db.session.commit()

    def validate_centro_creation(self, nombre, direccion, municipio):
        """valida que el centro no exista antes de agregarlo a la bd"""
        centro = Centro.query.filter(
            and_(
                and_(Centro.municipio == municipio, Centro.direccion == direccion),
                Centro.nombre == nombre,
            )
        ).first()
        return centro

    def show_one(self, id):
        """verifica si el centro ya existe"""
        centro = Centro.query.filter(
            and_(Centro.id == id, Centro.estado == "ACEPTADO")
        ).first()
        return centro

    def update_estado(self, centro_id, estado):
        """  modifica el estado a ACEPTADO o RECHAZADO """
        centro = Centro().find_by_id(centro_id)
        centro.estado = estado
        if estado == "ACEPTADO":
            centro.publicado = True
        else:
            centro.publicado = False
        db.session.commit()

    def update_publicado(self, centro_id, publicado):
        """ modifica el centro a publicado o despublicado - boolean - """
        centro = Centro().find_by_id(centro_id)
        if publicado == "True":
            centro.publicado = True
        else:
            centro.publicado = False
        db.session.commit()

    def validate_centro_update(self, nombre, direccion, municipio, id):
        """  valida que no exista centro con mismo municipio, dirección y nombre """
        centro = Centro.query.filter(
            and_(
                and_(
                    and_(Centro.municipio == municipio, Centro.direccion == direccion),
                    Centro.nombre == nombre,
                ),
                Centro.id != id,
            )
        ).first()
        return centro

    def eliminar(self, id):
        """elimina un centro pasandolo a activo=False"""
        turno = Turnos().turno_centro(id)
        for x in turno:
            x.estado = "CANCELADO"
        centro = Centro().find_by_id(id)
        centro.activo = False
        db.session.commit()
        return centro


def empty_value(data):
    """Valida que el campo en JSON no este vacio"""
    if not data:
        raise ValidationError("El campo no puede ser vacio.")


class CentroSchema(Schema):
    """ Esquema de centros para api marshmallow"""

    id = fields.Int()
    nombre = fields.Str(required=True, validate=empty_value)
    direccion = fields.Str(required=True, validate=empty_value)
    telefono = fields.Str()
    apertura = fields.DateTime(format="%H:%M", required=True, validate=empty_value)
    cierre = fields.DateTime(format="%H:%M", required=True, validate=empty_value)
    tipo_centro = fields.Str(required=True, validate=empty_value)
    web = fields.URL(required=False)
    email = fields.Email(required=False)
    latitud = fields.Float(required=True)
    longitud = fields.Float(required=True)
    id_municipio = fields.Int(required=True, validate=empty_value)
    pages = fields.Str()
    per_page = fields.Str()
    cantidad = fields.Int()


centro_schema = CentroSchema()
centros_schema = CentroSchema(many=True)
