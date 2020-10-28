from flask import redirect, flash, render_template, request, url_for, session, abort
from app.models.models import User
from app.models.configuracion import Configuracion
from app.resources.forms import FilterForm, RegistrationForm
from app.helpers.auth import authenticated
from flask_bcrypt import Bcrypt

# Protected resources
def index(page=1):
    if not authenticated(session):
        abort(401)
    form = FilterForm()
    sitio = Configuracion().sitio()
    if request.method == "POST":
        index_pag = User().search_by(form.username.data,form.estado.data, page, sitio.paginas)
    else:
        index_pag = User().all_paginado(page, sitio.paginas)
    return render_template("user/index.html", form=form, index_pag=index_pag)


def register():
    if not authenticated(session):
        abort(401)
    form = RegistrationForm()
    if form.validate_on_submit():
        if not validate(form):
            bcrypt = Bcrypt()
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode("utf-8")
            form.password.data = hashed_password
            flash("Usuario creado con éxito")
            create(form)
            return redirect(url_for("user_index", page=1))
        else:
            flash("El usuario o el email ya existe")
    return render_template("user/new.html", form=form)


def update(user_id):
    if not authenticated(session):
        abort(401)
    user = User.query.get_or_404(user_id)   #ver metodo
    form = RegistrationForm(obj=user)
    if form.validate_on_submit():
        if not user.validate_user_update(
            form.email.data, form.username.data, user_id
        ):
            bcrypt = Bcrypt()
            form.password.data = bcrypt.generate_password_hash(
                form.password.data
            ).decode("utf-8")
            form.populate_obj(user)
            User().update(user)
            return redirect(url_for("user_index", page=1))
        else:
            flash("El usuario o el email ya existe")
    return render_template("user/update.html", form=form)


def show():
    if not authenticated(session):
        abort(401)
    user = User().find_by_id(session.get("user_id"))
    return render_template("user/show.html", user=user)


def new():
    if not authenticated(session):
        abort(401)
    return render_template("user/new.html")


def create(form):
    if not authenticated(session):
        abort(401)
    user = User()
    user.create(form)

def validate(form):
    user = User().validate_user_creation(form["email"].data, form["username"].data)
    return user


def eliminar(user_id, page):
    User().eliminar(id=user_id)
    sitio = Configuracion().sitio()
    index_pag = User().all_paginado(page, sitio.paginas)
    flash("Usuario eliminado correctamente")
    form = FilterForm()
    return render_template("user/index.html",form=form, index_pag=index_pag, sitio=sitio)
    

def activar(user_id, page):
    User().activar(id=user_id)
    sitio = Configuracion().sitio()
    index_pag = User().all_paginado(page, sitio.paginas)
    flash("Usuario activado correctamente")
    form = FilterForm()
    return render_template("user/index.html",form=form, index_pag=index_pag)


def update_rol(user_id):
    if not authenticated(session):
        abort(401)
    roles = User().mis_roles(user_id)
    otros_roles = User().otros_roles(user_id)

    #print('mis roles:', roles)
    #print('mis no roles:', otros_roles)
    return render_template("user/update_rol.html",user_id=user_id, roles=roles, otros_roles=otros_roles)


def edit_roles(form):
    user = User().find_by_id(form.id)
    #print(user)
    #print(form.roles)
    #print('aca esta por entrar al')
    User.update_roles(form, user)
    #print('aca llegaaaaaaaaaaaaaaaaaaaaaaaa')
    update_rol(user_id=form.id)
