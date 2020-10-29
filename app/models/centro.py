from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    apertura = db.Column(db.DateTime, nullable=False)
    cierre = db.Column(db.DateTime, nullable=False)
    tipo_centro = db.Column(db.String(20), nullable=False)
    municipio = db.Column(db.String(20), nullable=False)
    web = db.Column(db.String(255), nullable=False)
    email = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    # protocolo = db.Column(db.String(255), nullable=False)
    coordenadas = db.Column(db.String(20), nullable=False)
    turnos = db.relationship("Bloque", backref="centro", lazy=True)


class Bloque(db.Model):
    __tablename__ = "bloque"
    id = db.Column(db.Integer, primary_key=True)
    franja = db.Column(db.String(255), nullable=False)  # franja de 30 en 30 min
    centro_id = db.Column(db.Integer, db.ForeignKey("centro.id"), nullable=False)