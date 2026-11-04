from django.apps import AppConfig


class App014SignalsConfig(AppConfig):
    name = 'app_015_signals'

    def ready(self):
        import app_015_signals.signals
