from django.apps import AppConfig


class GestionfermeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestionferme'
    verbose_name = 'Gestion de fermes'

    def ready(self):
        import gestionferme.signals
