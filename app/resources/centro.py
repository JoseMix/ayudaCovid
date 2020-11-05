import os
from werkzeug import secure_filename
from flask import Flask,redirect, flash, render_template, request, url_for, session, abort
# from app.db import connection
from app.models.configuracion import Configuracion
from app.models.centro import Centro
from app.helpers.auth import authenticated
from app.resources.forms import CrearCentroForm


def index(page):
    if not authenticated(session):
        abort(401)
    sitio = Configuracion().sitio()
    index_pag = Centro().all_paginado(page, sitio.paginas)    
    return render_template("centro/index.html", index_pag=index_pag)

def register():
    if not authenticated(session):
        abort(401)
    form = CrearCentroForm()
    if form.validate_on_submit():
        f = request.files['Protocolo'] 
        filename = secure_filename(f.filename)
        f.sase(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if not validate(form):
            flash("Centro creado con éxito")
            create(form)
            return redirect(url_for("centro_index", page=1))
        else:
            flash("El usuario o el email ya existe")
    return render_template("centro/new.html", form=form)

    

def validate(form):
    centro = Centro().validate_centro_creation(form["email"].data)
    return centro

def create(form):
    if not authenticated(session):
        abort(401)
    centro = Centro()
    centro.create(form)