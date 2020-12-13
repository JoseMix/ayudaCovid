
def authenticated(session):
    return session.get('user_id')


#verifica si usuario logueado tiene permiso
def tiene_permiso(session, permiso):
    if (permiso in session['permisos']):
        return True
    else:
        return False
