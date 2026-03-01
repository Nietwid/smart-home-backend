from django.apps import AppConfig


class DispatcherConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dispatcher"

    def ready(self):
        from dispatcher.handlers.cpu.events.device_connect import DeviceConnectEvent
        from dispatcher.handlers.cpu.events.device_disconnect import (
            DeviceDisconnectEvent,
        )
        from dispatcher.handlers.cpu.actions.update_peripheral import (
            UpdatePeripheralActionIntent,
            UpdatePeripheralActionResult,
        )
        from dispatcher.handlers.peripheria.actions.update_state import (
            UpdateStateActionIntent,
            UpdateStateActionResult,
        )
        from dispatcher.handlers.peripheria.actions.toggle import (
            ToggleActionIntent,
            ToggleActionResult,
        )
