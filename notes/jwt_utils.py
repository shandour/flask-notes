import jwt
from functools import wraps

from .models import User
from flask import request, abort, g, current_app as app


def jwt_required(view_func):
    @wraps(view_func)
    def decorated(*args, **kwargs):
        algorithm = app.config['JWT_ALGORITHM']
        key = app.config['JWT_KEY']

        g.user = None
        header = request.headers.get('Authorization', None)
        authenticated = False

        if not header:
            abort(401)

        token = header.split()[1]
        try:
            decoded = jwt.decode(token, key, algorithm=algorithm)
            user = User.query.filter(
                User.id == decoded['user_id']).scalar()
            if user:
                authenticated = True
                g.user = user
        except Exception as e:
            pass

        if authenticated:
            return view_func(*args, **kwargs)
        else:
            abort(401)
    return decorated
