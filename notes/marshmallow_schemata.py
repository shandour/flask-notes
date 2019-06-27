from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    ValidationError,
    decorators,
    post_load
)
from passlib.hash import argon2
from sqlalchemy.orm.exc import NoResultFound
from flask import current_app as app

import jwt

from .models import User


class NoteSchema(Schema):
    title = fields.String(validate=validate.Length(max=200))
    content = fields.String(required=True, validate=validate.Length(min=1))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    @post_load
    def generate_token(self, data, **kwargs):
        if self.user:
            data['user_id'] = self.user.id

        return data


class AuthMixin(Schema):
    username = fields.String(required=True,
                             validate=validate.Length(min=1, max=100))
    password = fields.String(required=True,
                             validate=validate.Length(min=1, max=100))


class RegisterSchema(AuthMixin):
    @validates('username')
    def validate_username(self, value):
        if User.query.filter(User.username == value).first():
            raise ValidationError('Username already taken')

        return value


class LoginSchema(AuthMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    @decorators.validates_schema
    def validate_fields(self, data):
        try:
            user = User.query.filter(User.username == data['username']).one()
        except NoResultFound:
            raise ValidationError('Username does not exist',
                                  field_names=['username'])

        password = data.get('password')
        if not password:
            raise ValidationError('Password required',
                                  field_names=['password'])
        if (
                not argon2.verify(
                    password,
                    user.password,
                )
        ):
            raise ValidationError('Incorrect credentials',
                                  field_names=['password'])

        self.user = user

    @post_load
    def generate_token(self, data, **kwargs):
        algorithm = app.config['JWT_ALGORITHM']
        key = app.config['JWT_KEY']
        data['token'] = jwt.encode(
            {'user_id': self.user.id},
            key,
            algorithm=algorithm
        ).decode('utf-8')

        return data
