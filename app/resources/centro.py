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

UPLOAD_FOLDER = "app/static/archivosPdf/"


def index():
    if not authenticated(session)or not tiene_permiso(session, 'centro_index'):
        abort(401)
    form = FilterFormCentro()
    sitio = Configuracion().sitio()
    page = request.args.get('page',1, type=int)
    mySearch = {}
    name = request.args.get("name")

    estado = request.args.get("estado")
    if name is None or name == '':
        name = ""
    if estado is None or estado == '':
        estado = ""
    
    mySearch["name"] = name
    mySearch["estado"] = estado
    if name != "" or estado != "" or request.method == "POST":
        #si estan seteados o se usó el buscador
        index_pag = Centro().search_by(name,estado,page,sitio.paginas)
    else:
        index_pag = Centro().all_paginado(page, sitio.paginas)
    return render_template("centro/index.html",form=form, mySearch=mySearch, index_pag=index_pag)


def register():
    if not authenticated(session)or not tiene_permiso(session, 'centro_new'):
        abort(401)
    form = CrearCentroForm()
    lista_municipio=show_municipio()
    if request.method == 'POST':
        if not validate(form):
            if validate_horarios(form): #Si los horarios ok
                file_protocolo = request.files['protocolo'] #Me quedo el archivo
                if validate_pdf(form,file_protocolo): #valido pdf
                    return redirect(url_for("centro_index", page=1))
                else:
                    return render_template("centro/new.html", form=form, lista_municipio=lista_municipio)
            else:                
                flash('El horario de apertura debe ser menor que el horario de cierre')
                return render_template("centro/new.html", form=form, lista_municipio=lista_municipio)
        else:
            flash("El centro que intenta crear ya existe.")
            return render_template("centro/new.html", form=form, lista_municipio=lista_municipio)
    else:        
        return render_template("centro/new.html", form=form, lista_municipio=lista_municipio)

def update(centro_id):    
    if not authenticated(session):
        abort(401)
    centro = Centro().query.get_or_404(centro_id)
    form = CrearCentroForm(obj=centro)
    viejo=str(form['protocolo'].data)
    #print("1:")
    print(viejo)
    #anterior=os.path.join(UPLOAD_FOLDER, viejo)
    #print("anterior:")
    #print(anterior)
    lista_municipio=show_municipio()
    if request.method == 'POST':
        if not centro.validate_centro_update(form.nombre.data, form.direccion.data, form.municipio.data , centro_id):           
            if validate_horarios(form):                
                file_protocolo = request.files['protocolo'] #Me quedo el archivo
                '''if file_protocolo:
                    if allowed_file(file_protocolo.filename):
                        #os.remove(anterior)
                        filename = secure_filename(file_protocolo.filename) #Me quedo con el nombre del pdf
                        file_protocolo.save(os.path.join(UPLOAD_FOLDER, filename))
                        #create(form, file_protocolo.filename)'''   
                form.populate_obj(centro)
                Centro().update(centro)               
                return redirect(url_for("centro_index", page=1))
            else:                
                flash('El horario de apertura debe ser menor que el horario de cierre')
                return render_template("centro/update.html", form=form, lista_municipio=lista_municipio)            
        else:
            flash("El centro ya existe")
    else:
        return render_template("centro/update.html", form=form,  centro_id=centro_id, lista_municipio=lista_municipio)

def validate_horarios(form):
    return form["apertura"].data < form["cierre"].data


def validate_pdf(form, file_protocolo):
    """Si el pdf esta ok almaceno con el file, sino en null"""
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
'''
def update_pdf(form,file_protocolo):
    Si el pdf esta ok almaceno con el file, sino en null
    if file_protocolo:
        if allowed_file(file_protocolo.filename):
            filename = secure_filename(file_protocolo.filename)
            file_protocolo.save(os.path.join(UPLOAD_FOLDER, filename))
            os.remove((app.config['UPLOAD_FOLDER']+Centro.id
            create(form, file_protocolo.filename)            
        else: 
            flash("El archivo debe ser pdf")    
            return False 
    else:
        create(form,"NULL") 
    flash("Centro creado con éxito")
    return True'''


def allowed_file(filename):
    # Chequeo de la extension y que solo exista un solo . antes de la extencion
    ALLOWED_EXTENSIONS = {"pdf"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate(form):
    centro = Centro().validate_centro_creation(
        form["nombre"].data, form["direccion"].data, form["municipio"].data
    )
    return centro


def create(form, nameProtocolo):
    if not authenticated(session) or not tiene_permiso(session, 'centro_new'):
        abort(401)
    centro = Centro()
    centro.create(form, nameProtocolo)


def show_municipio():
    data = requests.get(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios"
    ).json()
    lista = []
    for x in data["data"]["Town"]:
        muni = data["data"]["Town"][x]["name"]
        lista.append(muni)
    return lista


def show():
    if not authenticated(session)or not tiene_permiso(session, 'centro_show'):
        abort(401)
    centro = Centro().find_by_id(request.args.get("centro_id"))
    page = request.args.get("page", 1, type=int)
    # para no tener emails repetidos en el select
    select_email=[]
    for turno in centro.turnos:
        if (turno.email not in select_email):
            select_email.append(turno.email)
    sitio = Configuracion().sitio()
    search={}
        
    if request.args.get("email") is not None:
        search["email"]=request.args.get("email")
        turnos = Turnos().turnos_by_email(search["email"], request.args.get("centro_id"), page, sitio.paginas)
    else:
        search["email"]= "todos"
        turnos = Turnos().turnos_by_email("todos", request.args.get("centro_id"), page, sitio.paginas)
    return render_template(
        "centro/show.html", centro=centro, emails=select_email, index_pag=turnos, search=search)
