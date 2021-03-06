import os
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    redirect,
    flash,
    render_template,
    request,
    url_for,
    session,
    abort,
    json,
)
import requests

from app.models.configuracion import Configuracion
from app.models.centro import Turnos, Centro
from app.helpers.auth import authenticated, tiene_permiso
from app.resources.forms import CrearCentroForm, FilterFormCentro
from _datetime import date
import datetime

"""Rutas de los pdf"""
UPLOAD_FOLDER = "app/static/uploads/"
DOWNLOAD_FOLDER = "/static/uploads/"


def index():
    """Muestra el listado de centros e implementa la busqueda"""
    if not authenticated(session) or not tiene_permiso(session, "centro_index"):
        abort(401)
    form = FilterFormCentro()
    sitio = Configuracion().sitio()
    page = request.args.get("page", 1, type=int)
    mySearch = {}
    name = request.args.get("name")
    orden = request.args.get("orden")
    estado = request.args.get("estado")
    if name is None or name == "":
        name = ""
    if estado is None or estado == "":
        estado = ""
    if orden is None or orden == "":
        orden = "nombre"
    mySearch["name"] = name
    mySearch["estado"] = estado
    mySearch["orden"] = orden
    if name != "" or estado != "" or request.method == "POST":
        index_pag = Centro().search_by(name, estado, orden, page, sitio.paginas)
    else:
        index_pag = Centro().all_paginado(orden, page, sitio.paginas)
    lista_municipio = show_municipio()
    return render_template(
        "centro/index.html",
        form=form,
        mySearch=mySearch,
        index_pag=index_pag,
        municipios=lista_municipio,
    )


def register():
    """  Crea un centro validando que los horarios sean correctos, tenga pdf y no exista el centro """
    if not authenticated(session) or not tiene_permiso(session, "centro_new"):
        abort(401)
    form = CrearCentroForm()
    lista_municipio = show_municipio()
    if request.method == "POST":
        if not validate(form):
            if validate_horarios(form) and validate_tipo_centro(form.tipo_centro.data):
                if validate_pdf(form, request.files["protocolo"]):
                    return redirect(url_for("centro_index", page=1))
        else:
            flash("El centro que intenta crear ya existe.")
    return render_template(
        "centro/new.html", form=form, lista_municipio=lista_municipio
    )


def update(centro_id):
    """verifica si se puede actualaz y reenvia a vista udpate"""
    if not authenticated(session) or not tiene_permiso(session, "centro_update"):
        abort(401)
    lista_municipio = show_municipio()
    centro = Centro().query.get_or_404(centro_id)
    if centro.activo == False:
        abort(401)
    form = CrearCentroForm(obj=centro)
    if request.method != "POST":
        form.lat.data = centro.latitud
        form.lng.data = centro.longitud
        muni = get_municipio(form.municipio.data)
    if request.method == "POST":

        if update_centro(form, centro):
            flash("Centro modificado exitosamente!")
            return redirect(url_for("centro_index", page=1))

    return render_template(
        "centro/update.html",
        form=form,
        centro_id=centro_id,
        lista_municipio=lista_municipio,
        muni=muni,
    )


def update_centro(form, centro):
    """ valida los datos y actualiza """
    if not centro.validate_centro_update(
        form.nombre.data, form.direccion.data, form.municipio.data, centro.id
    ):
        if validate_horarios(form) and validate_tipo_centro(form.tipo_centro.data):
            if request.files["protocolo"]:  # si se carg?? protocolo
                file_protocolo = request.files["protocolo"]  # Me quedo el archivo
                if allowed_file(file_protocolo.filename):
                    if centro.protocolo != "NULL":
                        # si tiene protocolo viejo lo borra
                        path_viejo = os.path.join(UPLOAD_FOLDER, centro.protocolo)
                        os.remove(path_viejo)

                    filename = secure_filename(
                        file_protocolo.filename
                    )  # Me quedo con el nombre del pdf
                    file_protocolo.save(
                        os.path.join(UPLOAD_FOLDER, filename)
                    )  # guarda en carpeta
                    centro.protocolo = filename
            Centro().update(form, centro)  # actualiza centro
            return True
        else:
            return False
    else:
        flash("Ya existe un centro con nombre, direcci??n y municipio ingresado")
        return False


def validate_horarios(form):
    """ valida horario de apertura y cierre """
    if form["apertura"].data < form["cierre"].data:
        return True
    else:
        flash("El horario de apertura debe ser menor que el horario de cierre")
        return False


def validate_tipo_centro(tipo):
    """valida que se haya seleccionado un tipo de centro"""
    if tipo == "0":
        flash("No ha seleccionado un tipo de centro v??lido")
        return False
    else:
        return True


def validate_pdf(form, file_protocolo):
    """ Si el pdf esta ok almaceno con el file, sino en null """
    if file_protocolo:
        if allowed_file(file_protocolo.filename):
            filename = secure_filename(file_protocolo.filename)
            file_protocolo.save(os.path.join(UPLOAD_FOLDER, filename))
            create(form, file_protocolo.filename)
        else:
            flash("El archivo debe ser pdf")
            return False
    else:
        create(form, "NULL")
    flash("Centro creado con ??xito")
    return True


def allowed_file(filename):
    """ Chequeo de la extension y que solo exista un solo . (punto) antes de la extension """
    ALLOWED_EXTENSIONS = {"pdf"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate(form):
    """metodo que llama a la validacion del centro """
    centro = Centro().validate_centro_creation(
        form["nombre"].data, form["direccion"].data, form["municipio"].data
    )
    return centro


def create(form, nameProtocolo):
    """metodo que llama a la creacion del centro, formulario + protocolo"""
    if not authenticated(session) or not tiene_permiso(session, "centro_new"):
        abort(401)
    centro = Centro()
    centro.create(form, nameProtocolo)


def show_municipio():
    """retorna el listado de municipios de la api provista por la catedra"""
    data = requests.get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=135"
    ).json()
    lista = {}
    for x in data["data"]["Town"]:
        muni = data["data"]["Town"][x]["name"]
        lista[x] = muni
    return lista


def get_municipio(id):
    """ busca el nombre del municipio con id recibido por parametro """
    data = requests.get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=135"
    ).json()
    return data["data"]["Town"][str(id)]["name"]


def show():
    """muestra el centro con sus datos y turnos"""
    if not authenticated(session) or not tiene_permiso(session, "centro_show"):
        abort(401)
    centro = Centro().find_by_id(request.args.get("centro_id"))
    if centro == None:
        abort(404)
    municipio= get_municipio(centro.id)
    page = request.args.get("page", 1, type=int)
    if centro.protocolo:
        ruta = os.path.join(DOWNLOAD_FOLDER, centro.protocolo)
    else:
        ruta = "/"
    # para no tener emails repetidos en el select
    select_email = []
    for turno in centro.turnos:
        if turno.email not in select_email:
            select_email.append(turno.email)
    select_email.sort()
    sitio = Configuracion().sitio()
    search = {}

    if request.args.get("email") is not None:
        search["email"] = request.args.get("email")
        turnos = Turnos().turnos_by_email(
            search["email"], request.args.get("centro_id"), page, sitio.paginas
        )
    else:
        search["email"] = "todos"
        turnos = Turnos().turnos_by_email(
            "todos", request.args.get("centro_id"), page, sitio.paginas
        )
    return render_template(
        "centro/show.html",
        centro=centro,
        emails=select_email,
        index_pag=turnos,
        search=search,
        protocolo=ruta,
        municipio= municipio
    )


# elimina el centro
def eliminar(centro_id):
    """elimina un centro"""
    if not authenticated(session) or not tiene_permiso(session, "centro_destroy"):
        abort(401)
    Centro().eliminar(id=centro_id)
    flash("Centro eliminado y turnos cancelados correctamente")
    page = request.args.get("page", 1, type=int)
    name = request.args.get("name")
    estado = request.args.get("estado")
    return redirect(
        url_for(
            "centro_index", centro_id=centro_id, page=page, name=name, estado=estado
        )
    )


def update_estado():
    """ l??gica para aceptar o rechazar un centro """
    if not authenticated(session) or not tiene_permiso(session, "centro_update"):
        abort(401)
    Centro().update_estado(request.args.get("centro_id"), request.args.get("estado"))
    if request.args.get("estado") == "ACEPTADO":
        flash("??El centro de ayuda social ha sido aceptado exitosamente!")
    else:
        flash("??El centro de ayuda social ha sido rechazado exitosamente!")
    return redirect(url_for("centro_show", centro_id=request.args.get("centro_id")))


def update_publicado():
    """ l??gica para publicar o despublicar un centro """
    if not authenticated(session) or not tiene_permiso(session, "centro_update"):
        abort(401)

    Centro().update_publicado(
        request.args.get("centro_id"), request.args.get("publicado")
    )
    if request.args.get("publicado") == "True":
        flash("??El centro de ayuda social ha sido publicado exitosamente!")
    else:
        flash("??El centro de ayuda social ha sido despublicado exitosamente!")
    page = request.args.get("page", 1, type=int)
    name = request.args.get("name")
    estado = request.args.get("estado")
    return redirect(
        url_for(
            "centro_index",
            centro_id=request.args.get("centro_id"),
            page=page,
            name=name,
            estado=estado,
        )
    )
