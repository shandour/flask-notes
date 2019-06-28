import jwt
from functools import wraps

from .models import User
from flask import request, g, current_app as app, jsonify
from sqlalchemy.orm.exc import NoResultFound


def jwt_required(view_func):
    @wraps(view_func)
    def decorated(*args, **kwargs):
        algorithm = app.config['JWT_ALGORITHM']
        key = app.config['JWT_KEY']

        g.user = None
        header = request.headers.get('Authorization', None)
        authenticated = False

        if not header:
            return jsonify({'errors': 'Authorization header missing'}), 401

        token = header.split()[1]
        try:
            decoded = jwt.decode(token, key, algorithm=algorithm)
            user = User.query.filter(
                User.id == decoded['user_id']).scalar()
            if user:
                authenticated = True
                g.user = user
        except jwt.ExpiredSignatureError:
            return jsonify({'errors': 'Signature expired'}), 400
        except NoResultFound:
            return jsonify({'errors': 'User does not exists'}), 404

        if authenticated:
            return view_func(*args, **kwargs)
        else:
            return jsonify({'errors': 'Authorization failed'}), 401

    return decorated
