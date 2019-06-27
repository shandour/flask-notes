from flask import (
    jsonify,
    request,
    g,
    current_app as app
)
import jwt
from passlib.hash import argon2

from notes.blueprints import api_bp
from notes.celery_tasks import add_note, delete_note
from notes.marshmallow_schemata import NoteSchema, RegisterSchema, LoginSchema
from notes.models import User, Note, db
from notes.jwt_utils import jwt_required


@api_bp.route('/register', methods=['POST'])
def register():
    data, errors = RegisterSchema().load(request.form)

    if errors:
        return jsonify(errors), 400

    u = User(username=data['username'],
             password=argon2.hash(data['password']))
    db.session.add(u)
    db.session.commit()

    algorithm = app.config['JWT_ALGORITHM']
    key = app.config['JWT_KEY']

    token = jwt.encode(
        {'user_id': u.id},
        key,
        algorithm=algorithm
    ).decode('utf-8')

    return jsonify({
        'token': token
    }), 201


@api_bp.route('/login', methods=['POST'])
def login():
    data, errors = LoginSchema().load(request.form)

    if errors:
        return jsonify(errors), 400

    return jsonify({
        'token': data['token']
    }), 200


@api_bp.route('/notes', methods=['GET'])
@jwt_required
def display_notes():
    notes = Note.query.filter(Note.user_id == g.user.id).all()

    return jsonify({'notes': notes}), 200


@api_bp.route('/notes', methods=['POST'])
@jwt_required
def add_note_view():
    data, errors = NoteSchema(user=g.user).load(request.form)

    if errors:
        return jsonify(errors), 400

    add_note.delay(data)

    return '', 200


@api_bp.route('/notes/<uuid:note_id>', methods=['DELETE'])
@jwt_required
def delete_note_view(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user == g.user:
        delete_note.delay(note_id)
        return ''
    else:
        return '', 403
