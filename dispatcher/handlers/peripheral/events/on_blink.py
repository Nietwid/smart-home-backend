from dispatcher.device.messages.enum import MessageCommand
from dispatcher.device.messages.payload.lamp import OnBlinkPayload, OnBlinkStatus
from dispatcher.handlers.base import EventIntentBaseHandler
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
)
from dispatcher.handlers.registry import register_action_event
from notifier.enum import RabbitExchange, RabbitRoutingKey
from peripherals.models import Peripherals


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_BLINK,
)
class OnBlinkEventIntentHandler(EventIntentBaseHandler):
    exchange = RabbitExchange.SENSOR_SERVICE
    routing_key = RabbitRoutingKey.EVENTS

    def update_peripheral_state(self, peripheral: Peripherals, payload: OnBlinkPayload):
        if payload.status == OnBlinkStatus.START:
            peripheral.state["is_on"] = True
            peripheral.save(update_fields=["state"])
        elif payload.status == OnBlinkStatus.STOP:
            peripheral.state["is_on"] = False
            peripheral.save(update_fields=["state"])
