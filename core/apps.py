from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'
   
    def ready(self):
        # importa tus señales al arrancar Djan­go
        import core.signals
