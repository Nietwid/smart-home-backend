# consumers/apps.py
from django.apps import AppConfig


class ConsumersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "consumers"

    def ready(self):
        from consumers.rabbitmq_publisher import start_publisher

        start_publisher()
