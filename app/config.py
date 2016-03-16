from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'
    verbose_name = 'Api Application'

    def ready(self):
        from .signals import create_api_key
