from flask_sqlalchemy import SQLAlchemy
from operator import and_
from marshmallow import Schema, fields, ValidationError

db = SQLAlchemy()

# Inicializo contexto
def centro_turnos_initialize_db(app):
    app.app_context().push()
    db.init_app(app)
    db.create_all()


# Modelo Turnos de centros
class Turnos(db.Model):
    __tablename__ = "turnos"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    dia = db.Column(db.DateTime, nullable=False)
    estado = db.Column(
        db.Enum("VIGENTE", "CANCELADO"), nullable=False, default="VIGENTE"
    )
    turno_id = db.Column(db.Integer, db.ForeignKey("bloque.id"), nullable=False)
    centro_id = db.Column(db.Integer, db.ForeignKey("centro.id"), nullable=False)

    def create(self, form):
        turno = Turnos(
            email=form["email"],
            dia=form["dia"],
            turno_id=form["bloque"],
            centro_id=form["centro_id"],
        )
        db.session.add(turno)
        db.session.commit()

    # Baja lógica de turno
    def eliminar(self, id):
        turno = Turnos().find_by_id(id)
        turno.estado = "CANCELADO"
        db.session.commit()

    # busca turno por id
    def find_by_id(self, id):
        return Turnos.query.filter(Turnos.id == id).first()

    # Para validar turno repetido de centro
    def find_by(self, dia, bloque, centro_id):
        return Turnos.query.filter(
            and_(Turnos.centro_id == centro_id, Turnos.turno_id == bloque),
            Turnos.dia == dia,
            Turnos.estado == "VIGENTE",
        ).first()

    # busca turnos por email
    def turnos_by_email(self, email, centro_id, page, per_page):
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
        return Turnos.query.filter(
            and_(Turnos.dia == fecha, Turnos.centro_id == centro_id)
        ).all()

    def validar_turno_existente(self, id_bloque, id_centro, fecha):
        return Turnos.query.filter(
            and_(
                and_(Turnos.turno_id == id_bloque, Turnos.centro_id == id_centro),
                Turnos.dia == fecha,
            )
        ).first()


class TurnoSchema(Schema):
    centro_id = fields.Str()
    email = fields.Str()
    telefono = fields.Str()
    hora_inicio = fields.DateTime(format="%H:%M")
    hora_fin = fields.DateTime(format="%H:%M")
    fecha = fields.Date(format="%Y-%m-%d")


turno_schema = TurnoSchema()
turnos_schema = TurnoSchema(many=True)
# Modelo Bloque de turnos
class Bloque(db.Model):
    __tablename__ = "bloque"
    id = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    turnos = db.relationship("Turnos", backref="bloque", lazy=True)

    def all(self):
        return Bloque.query.all()

    def find_by_hora_inicio(self, hora):
        bloque = Bloque.query.filter_by(hora_inicio=hora).first()
        return bloque

    def bloques_ocupados(self, centro_id, fecha):
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


# Modelo Centro
class Centro(db.Model):
    __tablename__ = "centro"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    apertura = db.Column(db.Time, nullable=False)
    cierre = db.Column(db.Time, nullable=False)
    tipo_centro = db.Column(db.Enum("COMIDA", "ROPA", "PLASMA"), nullable=False)
    municipio = db.Column(db.String(20), nullable=False)
    web = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    estado = db.Column(
        db.Enum("RECHAZADO", "ACEPTADO", "PENDIENTE"),
        nullable=False,
        default="PENDIENTE",
    )
    publicado = db.Column(db.Boolean, nullable=False, default=False)
    activo = db.Column(db.Boolean, nullable=False, default=False)
    protocolo = db.Column(db.String(255), nullable=True)
    latitud = db.Column(db.String(20), nullable=True)
    longitud = db.Column(db.String(20), nullable=True)
    turnos = db.relationship("Turnos", backref="centro", lazy=True)

    def search_by(self, name, estado, page, per_page):
        if estado == "3":  # busco por nombre en todos los estados
            centro = (
                Centro()
                .query.filter(Centro.nombre.ilike(f"%{name}%"))
                .paginate(page=page, per_page=per_page, error_out=False)
            )
        else:
            if name == "":  # Si no vino nombre, busca solo por estado
                centro = (
                    Centro()
                    .query.filter(Centro.estado == estado)
                    .paginate(page=page, per_page=per_page, error_out=False)
                )
            else:  # vino nombre y estado
                centro = (
                    Centro()
                    .query.filter(
                        and_(Centro.nombre.ilike(f"%{name}%"), Centro.estado == estado)
                    )
                    .paginate(page=page, per_page=per_page, error_out=False)
                )
        return centro

    def all(self):
        centros = Centro.query.all()
        return centros

    def find_by_id(self, id):
        centro = Centro.query.filter(Centro.id == id).first()
        return centro

    # page= página actual, per_page = elementos x página
    def all_paginado(self, page, per_page):
        return Centro.query.order_by(Centro.id.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def create(self, formulario, nameProtocolo):
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
        centro = Centro.query.filter(
            and_(
                and_(Centro.municipio == municipio, Centro.direccion == direccion),
                Centro.nombre == nombre,
            )
        ).first()
        return centro

    def show_one(self, id):
        centro = Centro.query.filter(
            and_(Centro.id == id, Centro.estado == "ACEPTADO")
        ).first()
        return centro

    # modifica el estado a ACEPTADO o RECHAZADO
    def update_estado(self, centro_id, estado):
        centro = Centro().find_by_id(centro_id)
        centro.estado = estado
        if estado == "ACEPTADO":
            centro.publicado = True
        else:
            centro.publicado = False
        db.session.commit()

    # modifica el centro a publicado o despublicado - boolean -
    def update_publicado(self, centro_id, publicado):
        centro = Centro().find_by_id(centro_id)
        if publicado == "True":
            centro.publicado = True
        else:
            centro.publicado = False
        db.session.commit()

    # def update(self, centro):
    #    db.session.merge(centro)
    #    db.session.commit()

    # valida que no exista centro con mismo municipio, dirección y nombre
    def validate_centro_update(self, nombre, direccion, municipio, id):
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
        centro = Centro().find_by_id(id)
        centro.activo = False
        db.session.commit()
        return centro


def empty_value(data):
    if not data:
        raise ValidationError("El campo no puede ser vacio.")


class CentroSchema(Schema):
    nombre = fields.Str(required=True, validate=empty_value)
    direccion = fields.Str(required=True, validate=empty_value)
    telefono = fields.Str()
    apertura = fields.DateTime(format="%H:%M:%S", required=True, validate=empty_value)
    cierre = fields.DateTime(format="%H:%M:%S", required=True, validate=empty_value)
    tipo_centro = fields.Str(required=True, validate=empty_value)
    web = fields.Str()
    email = fields.Str()
    municipio = fields.Str(required=True, validate=empty_value)
    pages = fields.Str()
    per_page = fields.Str()


centro_schema = CentroSchema()
centros_schema = CentroSchema(many=True)