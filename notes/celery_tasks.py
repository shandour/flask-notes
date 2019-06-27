from notes.celery import celery
from notes.models import Note, db


@celery.task()
def add_note(validated_data):
    note = Note(**validated_data)
    db.session.add(note)
    db.session.commit()


@celery.task()
def delete_note(note_id):
    note = Note.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
