import click

from notes.models import db
from notes import create_app
from wsgi import app

@app.cli.command()
@click.confirmation_option(
    help='This action will create a new database. Are you sure?')
def create_db():
    "Creates the database"

    db.create_all()


@app.cli.command()
@click.confirmation_option(
    help='This action will drop the database. Are you sure?')
def drop_db():
    "Drops the database"

    db.drop_all()
