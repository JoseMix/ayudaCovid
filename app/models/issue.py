from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Issue(db.Model):
    __tablename__ = "issues"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(100))
    category_id = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, nullable=False)

    def all(conn):
        issues = Issue.query.all()
        return issues

    def create(conn, formulario):

        nuevo = Issue(
            email=formulario["email"],
            description=formulario["description"],
            category_id=formulario["category_id"],
            status_id=formulario["status_id"],
        )
        db.session.add(nuevo)
        db.session.commit()