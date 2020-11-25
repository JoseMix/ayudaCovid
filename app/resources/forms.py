from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TimeField, FloatField
from wtforms.validators import DataRequired, Length, Email, Regexp
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import EmailField, URLField, IntegerField

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
            Regexp("^[A-z][A-z|\.|\s]+$", message="El nombre no es válido"),
        ],
    )

    last_name = StringField(
        "Last name",
        validators=[
            DataRequired(message="El campo apellido no puede estar vacio"),
            Length(
                min=2, max=20, message="El Apellido debe tener entre 2-20 caracteres"
            ),
            Regexp("^[A-z][A-z|\.|\s]+$", message="El apellido no es válido"),
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
            DataRequired(message="El campo password no puede estar vacio"),
            Length(
                min=8, max=20, message="La password debe tener entre 8-20 caracteres"
            ),
        ],
    )
    submit = SubmitField("Enviar")


class FilterForm(FlaskForm):
    username = StringField()
    estado = SelectField(choices=[("2", "Todos"), ("1", "Activo"), ("0", "Bloqueado")])
    submit = SubmitField("Enviar")


class FilterFormCentro(FlaskForm):
    name = StringField()
    estado = SelectField(
        choices=[
            ("3", "Todos"),
            ("RECHAZADO", "RECHAZADO"),
            ("PENDIENTE", "PENDIENTE"),
            ("ACEPTADO", "ACEPTADO"),
        ]
    )
    submit = SubmitField("Enviar")


class CrearCentroForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El campo Nombre no puede estar vacio"),
            Length(min=2, max=25, message="El Nombre debe tener entre 2-25 caracteres"),
        ],
    )
    direccion = StringField(
        "Direccion",
        validators=[
            DataRequired(message="El Direccion email no puede estar vacio"),
            Length(
                min=2, max=20, message="La Direccion debe tener entre 2-20 caracteres"
            ),
        ],
    )
    telefono = IntegerField(
        "Telefono",
        validators=[
            DataRequired(message="El campo Telefono no puede estar vacio ni contener caracteres especiales")
        ],
    )

    apertura = TimeField(
        "Apertura",
        validators=[
            DataRequired(message="El campo Apertura no puede estar vacio"),
        ],
    )

    cierre = TimeField(
        "Cierre",
        validators=[
            DataRequired(message="El campo cierre no puede estar vacio"),
        ],
    )

    tipo_centro = SelectField(
        choices=[
            ("0", "elija una opcion"),
            ("COMIDA", "COMIDA"),
            ("ROPA", "ROPA"),
            ("PLASMA", "PLASMA"),
        ]
    )

    municipio = StringField(
        "Municipio",
        validators=[
            # DataRequired(message="El campo municipio no puede estar vacio"),
            Length(
                min=2, max=20, message="El municipio debe tener entre 8-10 caracteres"
            ),
        ],
    )
    web = URLField(
        "Web",
        validators=[
            Length(
                min=2, max=20, message="La web debe tener entre 8-20 caracteres"
            ),
        ],
    )

    email = EmailField(
        "Email",
        validators=[
            Email(message="El email no es valido"
            ),
        ],
    )

    protocolo = FileField("Protocolo")

    lng = FloatField()
    lat = FloatField()
    
    submit = SubmitField("Enviar")
