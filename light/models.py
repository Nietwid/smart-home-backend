from django.db import models
from button.models import ButtonType, MonostableButtonEvent, BistableButtonEvent
from consumers.router_message.builders.basic import get_intent_request
from consumers.router_message.message_event import MessageEvent
from consumers.device.messenger import DeviceMessenger
from device.models import Device


class Light(Device):
    button_type = models.CharField(
        max_length=5, choices=ButtonType.choices, default=ButtonType.BISTABLE
    )
    on = models.BooleanField(default=False)

    def available_events(self):
        if self.button_type == ButtonType.MONOSTABLE:
            return [event.value for event in MonostableButtonEvent]
        elif self.button_type == ButtonType.BISTABLE:
            return [event.value for event in BistableButtonEvent]
        else:
            return []

    def available_actions(self):
        return [
            MessageEvent.ON.value,
            MessageEvent.OFF.value,
            MessageEvent.TOGGLE.value,
        ]

    def make_intent(self, data: dict):
        intent = data.get("intent", None)
        if not intent:
            return
        message = None
        match intent:
            case MessageEvent.ON.value:
                self.on = True
                message = get_intent_request(MessageEvent.ON, self.mac)
            case MessageEvent.OFF.value:
                self.on = False
                message = get_intent_request(MessageEvent.OFF, self.mac)
        if message is not None:
            device_messenger = DeviceMessenger()
            device_messenger.send(self.get_router_mac(), message)
            self.save(update_fields=["on"])
