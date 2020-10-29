def authenticated(session):
    return session.get('user_id')
