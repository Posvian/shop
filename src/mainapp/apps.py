from django.apps import AppConfig
from django.core.signals import request_finished


class MainappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mainapp"

    def ready(self):
        import mainapp.signals
