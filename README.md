A Flask API for adding, dislaying an deleting notes with Celery.
Authorization is performed by using pyjwt JWT tokens. So please include the 2 following envvars to your app config; JWT_KEY for generating tokens and JWT_ALGORITHM.

A sample configuration:

Export relevant envvars:
export PROJECT_SETTINGS_FILE=../local_settings.py
export FLASK_APP=app.py


Local_settings.py:
SQLALCHEMY_ECHO = True
DEBUG = True
SECRET_KEY = '\xa6/\xee\xf3\x8d\xa6\xf1x\xa9P\xb6\xd6C\xf0VX\xcb\x1bK'
SQLALCHEMY_DATABASE_URI = "postgresql://myuser:mypass@localhost/flask-notes"
CELERY_BROKER_URL = 'amqp://localhost',
CELERY_RESULT_BACKEND = 'rpc://'
JWT_KEY = b'smth generated via os.urandom(512)'
JWT_ALGORITHM = 'HS512'


In one terminal: flask run
In the second one: celery worker -A app.celery -l info 
