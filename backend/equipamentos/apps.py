from django.apps import AppConfig

class EquipamentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'equipamentos'

    def ready(self):
        import equipamentos.signals  # Importa o arquivo signals.py
