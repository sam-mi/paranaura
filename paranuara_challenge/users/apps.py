from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'paranuara_challenge.users'
    verbose_name = "Users"

    def ready(self):
        from . import signals

    
