import os
from werkzeug.utils import secure_filename
from flask import Flask,redirect, flash, render_template, request, url_for, session, abort
# from app.db import connection
from app.models.configuracion import Configuracion
from app.models.centro import Turnos, Centro
from app.helpers.auth import authenticated
from app.resources.forms import CrearCentroForm
import requests
UPLOAD_FOLDER = "app/static/archivosPdf/" 


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
            if validate_horarios(form): #Si los horarios ok
                file_protocolo = request.files['protocolo'] #Me quedo con el nombre del archivo
                if validate_pdf(form,file_protocolo): #valido pdf
                    return redirect(url_for("centro_index", page=1))
                else:
                    return render_template("centro/new.html", form=form)
            else:
                flash('El horario de apertura debe ser menor que el horario de cierre')
                return render_template("centro/new.html", form=form)
        else:
            flash("El centro que intenta crear ya existe.")
            return render_template("centro/new.html", form=form)
    else:
        lista_municipio=show_municipio()
        return render_template("centro/new.html", form=form, lista_municipio=lista_municipio)

def validate_horarios(form):
    return (form['apertura'].data < form['cierre'].data)
    
def validate_pdf(form,file_protocolo):
    '''Si el pdf esta ok almaceno con el file, sino en null'''
    if file_protocolo:
        if allowed_file(file_protocolo.filename):
            filename = secure_filename(file_protocolo.filename)
            file_protocolo.save(os.path.join(UPLOAD_FOLDER, filename))
            create(form, file_protocolo.filename)
            
        else: 
            flash("El archivo debe ser pdf")    
            return False 
    else:
        create(form,"NULL") 
    flash("Centro creado con éxito")
    return True


def allowed_file(filename):
    #Chequeo de la extension y que solo exista un solo . antes de la extencion
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate(form):
    centro = Centro().validate_centro_creation(form["nombre"].data,form["direccion"].data,form["municipio"].data)
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
        

