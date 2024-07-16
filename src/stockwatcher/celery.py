from celery import Celery
from os import environ as env

env.setdefault("DJANGO_SETTINGS_MODULE", "stockwatcher.settings")

app = Celery("stockwatcher")
app.config_from_object("django.conf:settings")

app.autodiscover_tasks()
