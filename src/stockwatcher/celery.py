from os import environ as env
from celery import Celery
from celery.schedules import crontab

env.setdefault("DJANGO_SETTINGS_MODULE", "stockwatcher.settings")

app = Celery("stockwatcher")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "watch_all_stocks_every_minute": {
        "task": "stocks.tasks.watch_all_stocks_task",
        # "schedule": crontab(minute="*", day_of_week="mon-fri", hour="9-18"),
        "schedule": crontab(minute="*"),
    },
}
