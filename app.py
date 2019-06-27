# -*- coding: utf-8 -*-
from notes import create_app
from notes.celery import celery, init_celery

app = create_app()
init_celery(celery, app)

import manage
