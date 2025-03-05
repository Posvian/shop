import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(
    "config", broker="redis://127.0.0.1:6379", backend="redis://127.0.0.1:6379"
)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.timezone = "Europe/Moscow"

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# @app.task
# def add(x, y):
#     return x + y
