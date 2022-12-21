from django.apps import AppConfig


class RupyaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rupya'
    
    def ready(self) -> None:
        import rupya.signals