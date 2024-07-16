from celery import Celery
from os import environ as env

env.setdefault("DJANGO_SETTINGS_MODULE", "stockwatcher.settings")

app = Celery("stockwatcher")
app.config_from_object("django.conf:settings", namespace="CELERY")


@app.task
def test_task():
    return


app.autodiscover_tasks()
