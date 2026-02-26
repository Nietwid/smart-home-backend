from django.apps import AppConfig


class DispatcherConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dispatcher"

    def ready(self):
        from dispatcher.handlers.cpu.events.device_connect import DeviceConnectEvent
        from dispatcher.handlers.peripheria.actions.set_value import (
            SetValueActionIntent,
            SetValueActionResult,
        )
