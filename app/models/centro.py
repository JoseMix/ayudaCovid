from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()
ma = Marshmallow()

# Inicializo contexto
def centro_bloque_initialize_db(app):
    app.app_context().push()
    db.init_app(app)
    db.create_all()


class Centro(db.Model):
    __tablename__ = "centro"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    direccion = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    apertura = db.Column(db.String(20), nullable=False)
    cierre = db.Column(db.String(20), nullable=False)
    tipo_centro = db.Column(db.String(20), nullable=False)
    municipio = db.Column(db.String(20), nullable=False)
    web = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    # protocolo = db.Column(db.String(255), nullable=False)
    coordenadas = db.Column(db.String(20), nullable=False)
    turnos = db.relationship("Bloque", backref="centro", lazy=True)

    def all(self):
        centros = Centro.query.all()
        return centros

    def showOne(self, id):
        centro = Centro.query.filter_by(id=id).first()
        return centro


class Bloque(db.Model):
    __tablename__ = "bloque"
    id = db.Column(db.Integer, primary_key=True)
    franja = db.Column(db.String(255), nullable=False)  # franja de 30 en 30 min
    centro_id = db.Column(db.Integer, db.ForeignKey("centro.id"), nullable=False)


class CentroSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Centro
        include_relationships = False
        load_instance = True


centro_schema = CentroSchema()
centros_schema = CentroSchema(many=True)