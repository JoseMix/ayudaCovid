from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    def __getitem__(self, email):
        return self.__dict__[email]

    def find_by_email_and_pass(self, conn, emailForm, passwordForm):
        user = User.query.filter(
            and_(User.email == emailForm, User.password == passwordForm)
        ).first()
        return user

    def all(conn):
        users = User.query.all()
        return users

    def create(conn, formulario):
        nuevo = User(
            email=formulario["email"],
            password=formulario["password"],
            first_name=formulario["first_name"],
            last_name=formulario["last_name"],
        )
        db.session.add(nuevo)
        db.session.commit()
