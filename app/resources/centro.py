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

# from app.db import connection
from app.models.configuracion import Configuracion
from app.models.centro import Turnos, Centro
from app.helpers.auth import authenticated, tiene_permiso
from app.resources.forms import CrearCentroForm, FilterFormCentro

import requests
from _datetime import date
import datetime

# para local
UPLOAD_FOLDER = "app/static/uploads/"

# para producción
#UPLOAD_FOLDER = "/home/grupo13.proyecto2020.linti.unlp.edu.ar/app/static/uploads/"


def index():
    if not authenticated(session) or not tiene_permiso(session, "centro_index"):
        abort(401)
    form = FilterFormCentro()
    sitio = Configuracion().sitio()
    page = request.args.get("page", 1, type=int)
    mySearch = {}
    name = request.args.get("name")

    estado = request.args.get("estado")
    if name is None or name == "":
        name = ""
    if estado is None or estado == "":
        estado = ""

    mySearch["name"] = name
    mySearch["estado"] = estado
    if name != "" or estado != "" or request.method == "POST":
        # si estan seteados o se usó el buscador
        index_pag = Centro().search_by(name, estado, page, sitio.paginas)
    else:
        index_pag = Centro().all_paginado(page, sitio.paginas)
    return render_template(
        "centro/index.html", form=form, mySearch=mySearch, index_pag=index_pag
    )



def register():
    """  vista del formulario y lógica de create de centro """
    if not authenticated(session) or not tiene_permiso(session, "centro_new"):
        abort(401)

    form = CrearCentroForm()
    lista_municipio = show_municipio()

    if request.method == "POST":
        if not validate(form):  # valida que no exista centro con mismos datos
            if validate_horarios(form) and validate_tipo_centro(
                form.tipo_centro.data
            ):  # Si los horarios ok
                if validate_pdf(
                    form, request.files["protocolo"]
                ):  # valido pdf y crea centro
                    return redirect(url_for("centro_index", page=1))
        else:
            flash("El centro que intenta crear ya existe.")
    return render_template(
        "centro/new.html", form=form, lista_municipio=lista_municipio
    )


def update(centro_id):
    if not authenticated(session) or not tiene_permiso(session, "centro_update"):
        abort(401)
    lista_municipio = show_municipio()
    # busca el centro y carga el formulario de update
    centro = Centro().query.get_or_404(centro_id)
    if(centro.activo == False ):
        abort(401)
    form = CrearCentroForm(obj=centro)
    if request.method != "POST":
        form.lat.data = centro.latitud
        form.lng.data = centro.longitud
        muni = get_municipio(form.municipio.data)
    if request.method == "POST":
        # valida y modifica, retorna boolean
        if update_centro(form, centro):
            return redirect(url_for("centro_index", page=1))
        #si falla alguna validación que redireccione al update
    return render_template(
        "centro/update.html",
        form=form,
        centro_id=centro_id,
        lista_municipio=lista_municipio,muni = muni
    )



def update_centro(form, centro):
    """ valida los datos y modifica si todo OK """
    if not centro.validate_centro_update(
        form.nombre.data, form.direccion.data, form.municipio.data, centro.id
    ):
        if validate_horarios(form) and validate_tipo_centro(form.tipo_centro.data):
            if request.files["protocolo"]:  # si se cargó protocolo
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
        flash("Ya existe un centro con nombre, dirección y municipio ingresado")
        return False



def validate_horarios(form):
    """ valida horario de apertura y cierre. retorna boolean """
    if form["apertura"].data < form["cierre"].data:
        return True
    else:
        flash("El horario de apertura debe ser menor que el horario de cierre")
        return False


def validate_tipo_centro(tipo):
    if tipo == "0":
        flash("No ha seleccionado un tipo de centro válido")
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
    flash("Centro creado con éxito")
    return True


def allowed_file(filename):
    """ Chequeo de la extension y que solo exista un solo . antes de la extension """
    ALLOWED_EXTENSIONS = {"pdf"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate(form):
    centro = Centro().validate_centro_creation(
        form["nombre"].data, form["direccion"].data, form["municipio"].data
    )
    return centro


def create(form, nameProtocolo):
    if not authenticated(session) or not tiene_permiso(session, "centro_new"):
        abort(401)
    centro = Centro()
    centro.create(form, nameProtocolo)


def show_municipio():
    data = requests.get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=135"
    ).json()
    lista = {}
    for x in data["data"]["Town"]:
        muni = data["data"]["Town"][x]["name"]
        lista[x] = muni
    return lista


def get_municipio(id):
    """ busca el nombre del municipio con id recibido por parametro. returna string """
    data = requests.get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=135"
    ).json()
    return data["data"]["Town"][str(id)]["name"]

def show():
    if not authenticated(session) or not tiene_permiso(session, "centro_show"):
        abort(401)
    centro = Centro().find_by_id(request.args.get("centro_id"))
    if centro == None:
        abort(404)
    page = request.args.get("page", 1, type=int)
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
    )


# elimina el centro
def eliminar(
    centro_id,
):
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
    """ lógica para aceptar o rechazar un centro """
    if not authenticated(session) or not tiene_permiso(session, "centro_update"):
        abort(401)
    Centro().update_estado(request.args.get("centro_id"), request.args.get("estado"))
    if request.args.get("estado") == "ACEPTADO":
        flash("¡El centro de ayuda social ha sido aceptado exitosamente!")
    else:
        flash("¡El centro de ayuda social ha sido rechazado exitosamente!")
    return redirect(url_for("centro_show", centro_id=request.args.get("centro_id")))



def update_publicado():
    """ lógica para publicar o despublicar un centro """
    if not authenticated(session) or not tiene_permiso(session, "centro_update"):
        abort(401)

    Centro().update_publicado(
        request.args.get("centro_id"), request.args.get("publicado")
    )
    if request.args.get("publicado") == "True":
        flash("¡El centro de ayuda social ha sido publicado exitosamente!")
    else:
        flash("¡El centro de ayuda social ha sido despublicado exitosamente!")
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
