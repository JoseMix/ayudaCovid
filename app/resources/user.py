from flask import redirect, flash, render_template, request, url_for, session, abort
from app.models.models import User
from app.models.configuracion import Configuracion
from app.resources.forms import FilterForm, RegistrationForm
from app.helpers.auth import authenticated
from flask_bcrypt import Bcrypt

# Protected resources
def index():
    if not authenticated(session):
        abort(401)
    form = FilterForm()
    sitio = Configuracion().sitio()

    page = request.args.get('page',1, type=int)
    mySearch = {}
    username = request.args.get("username")

    estado = request.args.get("estado")
    if username is None or username == '':
        username = ""
    if estado is None or estado == '':
        estado = ""
    
    mySearch["username"] = username
    mySearch["estado"] = estado
    if username != "" or estado != "" or request.method == "POST":
        #si estan seteados o se usó el buscador
        index_pag = User().search_by(username,estado, page, sitio.paginas)
    else:
        index_pag = User().all_paginado(page, sitio.paginas)

    return render_template("user/index.html",form=form, mySearch=mySearch, index_pag=index_pag)


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
            return redirect(url_for("user_index", page=1, username='vacio'))
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
            return redirect(url_for("user_index", page=1, username='vacio'))
        else:
            flash("El usuario o el email ya existe")
    return render_template("user/update.html", form=form, user_id=user_id)


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
    #busco si el usuario tiene rol admin
    user = User().is_admin(user_id)
    if user:
        flash("no se puede eliminar, usuario administrador")
    else:
        User().eliminar(id=user_id)
        flash("Usuario eliminado correctamente")
    sitio = Configuracion().sitio()
    index_pag = User().all_paginado(page, sitio.paginas)
    form = FilterForm()
    mySearch = {}
    mySearch["username"] = request.args.get("username")
    mySearch["estado"] = request.args.get("estado")
    return render_template("user/index.html",form=form, index_pag=index_pag, sitio=sitio, mySearch=mySearch)


def activar(user_id, page):
    User().activar(id=user_id)
    sitio = Configuracion().sitio()
    index_pag = User().all_paginado(page, sitio.paginas)
    flash("Usuario activado correctamente")
    form = FilterForm()
    mySearch = {}
    mySearch["username"] = request.args.get("username")
    mySearch["estado"] = request.args.get("estado")
    return render_template("user/index.html",form=form, index_pag=index_pag, mySearch=mySearch)


def update_rol(user_id):
    if not authenticated(session):
        abort(401)
    roles = User().mis_roles(user_id)
    #otros_roles = User().otros_roles(user_id)
    if request.method == "POST":
        user = User().find_by_id(user_id) #busco el usuario para modificar roles
        form = request.form
        print(form)
        
        for rol in form:
            #print(rol)
            User().delete_rol(rol, user)
        roles = User().mis_roles(user_id)

        #User().add_rol(form['otros_roles'],user)
    return render_template("user/update_rol.html",user_id=user_id, roles=roles)
