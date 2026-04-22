from django.apps import AppConfig


class MtappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "mtapp"

    def ready(self):
        import mtapp.signal
