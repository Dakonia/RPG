from django.apps import AppConfig

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'  # Исправлено на 'news'

    def ready(self):
        from . import signals