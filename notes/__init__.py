# -*- coding: utf-8 -*-
from flask import Flask


def create_app(settings_module='notes.settings'):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    if not app.testing:
        app.config.from_envvar('PROJECT_SETTINGS_FILE')

    from notes.models import db
    db.init_app(app)

    import notes.views
    from notes.blueprints import api_bp
    app.register_blueprint(api_bp)

    key = app.config.get('JWT_KEY')
    algorithm = app.config.get('JWT_ALGORITHM')
    if not key or not algorithm:
        raise Exception(
            'improperly configured. '
            'Please specify the JWT_KEY and JWT_ALGORITHM value'
        )

    return app
