def authenticated(session):
    """returna el id del usuario logueado"""
    return session.get("user_id")


def tiene_permiso(session, permiso):
    """verifica si usuario logueado tiene permiso"""
    if permiso in session["permisos"]:
        return True
    else:
        return False
