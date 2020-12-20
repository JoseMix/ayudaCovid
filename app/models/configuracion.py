from flask_sqlalchemy import SQLAlchemy
from datetime import date
from marshmallow import Schema, fields, ValidationError


db = SQLAlchemy()


def configuracion_initialize_db(app):
    """ Inicializo contexto"""
    app.app_context().push()
    db.init_app(app)
    db.create_all()


# Modelo configuracion
class Configuracion(db.Model):
    """ Modelo configuracion de sitio"""

    __tablename__ = "configuracion"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    email = db.Column(db.String(255))
    paginas = db.Column(db.Integer)
    activo = db.Column(db.Boolean, nullable=False)

    def create(self, formulario):
        """crea nueva configuracion del sitio"""
        nuevo = Configuracion(
            email=formulario["email"],
            titulo=formulario["titulo"],
            descripcion=formulario["descripcion"],
            activo=eval(formulario["activo"]),
            paginas=formulario["paginado"],
        )
        db.session.add(nuevo)
        db.session.commit()

    def sitio(self):
        """retorna la configuracion del sitio"""
        sitio = Configuracion.query.first()
        return sitio

    def edit(self, formulario):
        """edita la configuracion del sitio"""
        sitio = self.sitio()
        sitio.email = formulario["email"]
        sitio.titulo = formulario["titulo"]
        sitio.descripcion = formulario["descripcion"]
        sitio.activo = eval(formulario["activo"])
        sitio.paginas = formulario["paginas"]
        db.session.commit()


def empty_value(data):
    """Valida que el campo en JSON no este vacio"""
    if not data:
        raise ValidationError("El campo no puede ser vacio.")

class SitioSchema(Schema):
    """ Esquema de configuración de sitio para api marshmallow"""

    titulo = fields.Str(required=True, validate=empty_value)
    descripcion = fields.Str(required=True, validate=empty_value)
    email = fields.Email(required=True, validate=empty_value)
    paginas = fields.Int(required=True, validate=empty_value)
    activo = fields.Boolean(required=True, validate=empty_value)

sitio_schema = SitioSchema()