from celery import Celery
from os import environ as env

# from celery.schedules import crontab

env.setdefault("DJANGO_SETTINGS_MODULE", "stockwatcher.settings")

app = Celery("stockwatcher")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "watch_stock_every_minute": {
        "task": "watcher.tasks.watch_stock",
        "schedule": 60.0,
        "args": ("ASX", "ASX", "USD"),
    }
}
