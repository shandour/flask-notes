# -*- coding: utf-8 -*-
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


db = SQLAlchemy()

#notes_users = db.Table(
 #   'notes_users',
  #  db.Column('user_id', db.Integer, db.ForeignKey('users.id'),
   #           primary_key=True),
    #db.Column('note_id', UUID, db.ForeignKey('notes.id'),
     #         primary_key=True))


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f'<Note id={self.id}>'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(130))
    notes = db.relationship('Note', backref='user')
