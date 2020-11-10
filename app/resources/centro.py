import os
from werkzeug.utils import secure_filename
from flask import Flask,redirect, flash, render_template, request, url_for, session, abort
# from app.db import connection
from app.models.configuracion import Configuracion
from app.models.centro import Centro
from app.helpers.auth import authenticated
from app.resources.forms import CrearCentroForm
import app, requests
UPLOAD_FOLDER = "app/static/archivosPdf/" #Cambiar la carpeta a statics
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

def index(page):
    if not authenticated(session):
        abort(401)
    sitio = Configuracion().sitio()
    index_pag = Centro().all_paginado(page, sitio.paginas) 
    show_municipio()   
    return render_template("centro/index.html", index_pag=index_pag)

def register():
    if not authenticated(session):
        abort(401)
    form = CrearCentroForm()
    if request.method == 'POST':
        if not validate(form):
            file_protocolo = request.files['protocolo'] #Me quedo con el nombre del archivo
            if file_protocolo:
                if allowed_file(file_protocolo.filename): #Si esta todo ok 
                    filename = secure_filename(file_protocolo.filename)
                    file_protocolo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #Se almacena el arch en la carpeta
                    flash("Centro creado con éxito")
                    create(form, file_protocolo.filename)  
                    return redirect(url_for("centro_index", page=1))
                else: flash("El archivo debe ser pdf")    
            else:  #El protocolo no es obligatorio, llamar a crear con null en el protocolo
                create(form,"NULL")   
                return redirect(url_for("centro_index", page=1))   
        else:
            flash("El email del centro ya existe")
    lista_municipio=show_municipio()
    return render_template("centro/new.html", form=form, lista_municipio=lista_municipio)

def allowed_file(filename):
    #Chequeo de la extension y que solo exista un solo . antes de la extencion
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate(form):
    centro = Centro().validate_centro_creation(form["email"].data)
    return centro

def create(form,nameProtocolo):
    if not authenticated(session):
        abort(401)
    centro = Centro()
    centro.create(form,nameProtocolo)


def show_municipio():
    data = requests.get("https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios").json()
    lista=[]
    for x in data["data"]["Town"]: 
        muni=data["data"]["Town"][x]["name"]
        lista.append(muni)
    return lista
        

