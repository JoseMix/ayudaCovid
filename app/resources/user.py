from flask import redirect, flash, render_template, request, url_for, session, abort
from app.models.models import Rol, User
from app.models.configuracion import Configuracion
from app.resources.forms import FilterForm, RegistrationForm
from app.helpers.auth import authenticated, tiene_permiso
from flask_bcrypt import Bcrypt


def index():
    """controlador que verifica si esta logueado, tienes permisos y lista los usuarios"""
    if not authenticated(session) or not tiene_permiso(session, "user_index"):
        abort(401)
    form = FilterForm()
    sitio = Configuracion().sitio()

    page = request.args.get("page", 1, type=int)
    mySearch = {}
    username = request.args.get("username")
    orden = request.args.get("orden")
    estado = request.args.get("estado")
    if username is None or username == "":
        username = ""
    if estado is None or estado == "":
        estado = ""
    if orden is None or orden == "":
        orden = "username"
    mySearch["username"] = username
    mySearch["estado"] = estado
    mySearch["orden"] = orden
    if username != "" or estado != "" or request.method == "POST":

        index_pag = User().search_by(username, estado, orden, page, sitio.paginas)
    else:
        index_pag = User().all_paginado(orden, page, sitio.paginas)
    return render_template(
        "user/index.html", form=form, mySearch=mySearch, index_pag=index_pag
    )


def register():
    """controlador que verifica si esta logueado, tienes permisos y registra un usuario"""
    if not authenticated(session) or not tiene_permiso(session, "user_new"):
        abort(401)
    form = RegistrationForm()
    if form.validate_on_submit():
        if not validate(form):
            bcrypt = Bcrypt()
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            form.password.data = hashed_password
            flash("Usuario creado con éxito")
            create(form)
            return redirect(url_for("user_index", page=1))
        else:
            flash("El usuario o el email ya existe")
    return render_template("user/new.html", form=form)


def update(user_id):
    """controlador que verifica si esta logueado, tienes permisos y actualiza un usuario"""
    if not authenticated(session) or not tiene_permiso(session, "user_update"):
        abort(401)
    user = User.query.get_or_404(user_id)  # ver metodo
    form = RegistrationForm(obj=user)
    if form.validate_on_submit():
        if not user.validate_user_update(form.email.data, form.username.data, user_id):
            bcrypt = Bcrypt()
            form.password.data = bcrypt.generate_password_hash(
                form.password.data
            ).decode("utf-8")
            form.populate_obj(user)
            User().update(user)
            flash("Usuario modificado exitosamente!")
            return redirect(url_for("user_index", page=1))
        else:
            flash("El usuario o el email ya existe")
    return render_template("user/update.html", form=form, user_id=user_id)


def show():
    """controlador que verifica si esta logueado, tienes permisos y busca usuarios por id"""
    if not authenticated(session) or not tiene_permiso(session, "user_show"):
        abort(401)
    user = User().find_by_id(session.get("user_id"))
    return render_template("user/show.html", user=user)


def new():
    """controlador que verifica si esta logueado y tienes permisos"""
    if not authenticated(session) or not tiene_permiso(session, "user_new"):
        abort(401)
    return render_template("user/new.html")


def create(form):
    """controlador que verifica si esta logueado, tienes permisos y crea un usuario"""
    if not authenticated(session) or not tiene_permiso(session, "user_new"):
        abort(401)
    user = User()
    user.create(form)


def validate(form):
    """controlador que valida si el usuario existe"""
    user = User().validate_user_creation(form["email"].data, form["username"].data)
    return user


def eliminar(user_id, page):
    """
    controlador que verifica si esta logueado, tienes permisos y elimina un usuario,
    en caso de que sea admin verifica que no sea el unico
    """
    if not authenticated(session) or not tiene_permiso(session, "user_destroy"):
        abort(401)
    user = User().tiene_rol(user_id, "administrador")
    if user:
        flash("no se puede eliminar, usuario administrador")
    else:
        User().eliminar(id=user_id)
        flash("Usuario eliminado correctamente")
    sitio = Configuracion().sitio()

    form = FilterForm()
    mySearch = {}
    mySearch["username"] = request.args.get("username")
    mySearch["estado"] = request.args.get("estado")
    mySearch["orden"] = request.args.get("orden")
    index_pag = User().all_paginado(mySearch["orden"], page, sitio.paginas)
    return render_template(
        "user/index.html",
        form=form,
        index_pag=index_pag,
        sitio=sitio,
        mySearch=mySearch,
    )


def activar(user_id, page):
    """controlador que verifica si esta autenticado, tiene permisos y activa al usuario"""
    if not authenticated(session) or not tiene_permiso(session, "user_update"):
        abort(401)
    User().activar(id=user_id)
    sitio = Configuracion().sitio()

    flash("Usuario activado correctamente")
    form = FilterForm()
    mySearch = {}
    mySearch["username"] = request.args.get("username")
    mySearch["estado"] = request.args.get("estado")
    mySearch["orden"] = request.args.get("orden")
    index_pag = User().all_paginado(mySearch["orden"], page, sitio.paginas)
    return render_template(
        "user/index.html", form=form, index_pag=index_pag, mySearch=mySearch
    )


def update_rol(user_id):
    """controlador que muestra vista para roles y, si se oprime submit, modifica roles de usuario"""
    if not authenticated(session) or not tiene_permiso(session, "user_update"):
        abort(401)
    roles = Rol().all()
    user = User().find_by_id(user_id)

    if request.method == "POST":
        form = request.form
        checked = []
        for rol in form:
            act = Rol().find_by_id(form[rol])
            checked.append(act)

        for rol in roles:
            if rol not in checked:
                if rol in user.roles:
                    if Rol().is_admin(rol.id) and not (
                        User().unico_admin(rol.id, user_id)
                    ):
                        flash(
                            "No se puede eliminar el rol administrador al usuario. es el unico administrador"
                        )
                    else:
                        User().delete_rol(rol, user)

        for rol in checked:
            if rol not in user.roles:
                User().add_rol(rol, user)
        flash("La modificación de roles fue exitosa!")
        user = User().find_by_id(user_id)
    return render_template("user/update_rol.html", user=user, roles=roles)
