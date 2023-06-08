from django.apps import AppConfig


class UtulisateursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'utulisateurs'

    def ready(self):
        import utulisateurs.signals
