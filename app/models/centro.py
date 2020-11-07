from flask_sqlalchemy import SQLAlchemy
from operator import and_

db = SQLAlchemy()


# Inicializo contexto
def centro_bloque_initialize_db(app):
    app.app_context().push()
    db.init_app(app)
    db.create_all()


class Centro(db.Model):
    __tablename__ = "centro"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    apertura = db.Column(db.Time, nullable=False)
    cierre = db.Column(db.Time, nullable=False)
    tipo_centro = db.Column(db.String(20), nullable=False)
    municipio = db.Column(db.String(20), nullable=False)
    web = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Enum("RECHAZADO","ACEPTADO","PENDIENTE","PUBLICADO","DESPUBLICADO"), nullable=False)
    protocolo = db.Column(db.String(255), nullable=False)
    coordenadas = db.Column(db.String(20), nullable=False)
    turnos = db.relationship("Bloque", backref="centro", lazy=True)

    def all(self):
        centros = Centro.query.all()
        return centros

    #page= página actual, per_page = elementos x página
    def all_paginado(self , page, per_page):
        return Centro.query.order_by(Centro.id.asc()).\
            paginate(page=page, per_page=per_page, error_out=False)

    def create(self, formulario, nameProtocolo):
        nuevo = Centro(
            nombre =formulario["nombre"].data,
            direccion=formulario["direccion"].data,
            telefono=formulario["telefono"].data,
            apertura=formulario["apertura"].data,
            cierre=formulario["cierre"].data,
            tipo_centro=formulario["tipo_centro"].data,
            municipio=formulario["municipio"].data,
            web=formulario["web"].data,
            email=formulario["email"].data,
            estado="PENDIENTE",
            protocolo=nameProtocolo,
            coordenadas="NULL",
        )
        db.session.add(nuevo)
        db.session.commit()

    def validate_centro_creation(self, nombre,direccion,municipio):
        centro = Centro.query.filter(and_(and_(Centro.municipio == municipio,Centro.direccion==direccion),Centro.nombre==nombre)).first()
        return centro

class Bloque(db.Model):
    __tablename__ = "bloque"
    id = db.Column(db.Integer, primary_key=True)
    franja = db.Column(db.String(255), nullable=False)  # franja de 30 en 30 min
    centro_id = db.Column(db.Integer, db.ForeignKey("centro.id"), nullable=False)