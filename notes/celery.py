import os
from celery import Celery


def make_celery(app_name=__name__):
    return Celery(
        app_name,
        backend=os.environ.get('CELERY_RESULT_BACKEND'),
        broker=os.environ.get('CELERY_BROKER_URL')
    )


def init_celery(celery, app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask


celery = make_celery()
