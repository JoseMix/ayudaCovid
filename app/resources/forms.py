from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="El campo username no puede estar vacio"),
            Length(
                min=4, max=20, message="El Username debe tener entre 4-20 caracteres"
            ),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El campo email no puede estar vacio"),
            Email(message="El Email no es Valido"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="El campo password no puede estar vacio"),
            Length(
                min=8, max=20, message="La Password debe tener entre 8-20 caracteres"
            ),
        ],
    )
    first_name = StringField(
        "First name",
        validators=[
            DataRequired(message="El campo nombre no puede estar vacio"),
            Length(min=2, max=20, message="El Nombre debe tener entre 2-20 caracteres"),
        ],
    )
    last_name = StringField(
        "Last name",
        validators=[
            DataRequired(message="El campo apellido no puede estar vacio"),
            Length(
                min=2, max=20, message="El Apellido debe tener entre 2-20 caracteres"
            ),
        ],
    )

    submit = SubmitField("Enviar")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El campo email no puede estar vacio"),
            Email(message="Introduzca un email"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=20, message="El Nombre debe tener entre 8-20 caracteres"),
        ],
    )
    submit = SubmitField("Enviar")

class FilterForm(FlaskForm):
    nombre = StringField()   
    submit = SubmitField("Enviar")