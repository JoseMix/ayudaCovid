from flask import redirect, flash, render_template, request, url_for, session, abort
# from app.db import connection
from app.models.configuracion import Configuracion
from app.models.centro import Centro
from app.helpers.auth import authenticated
from app.models.models import User
from flask_bcrypt import Bcrypt

def index(page):
    if not authenticated(session):
        abort(401)
    sitio = Configuracion().sitio()
    index_pag = Centro().all_paginado(page, sitio.paginas)    
    return render_template("centro/index.html", index_pag=index_pag)