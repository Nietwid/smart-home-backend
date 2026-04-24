from datetime import datetime

from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.builder.rfid import rfid_message_builder
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
    MessageCommand,
)
from dispatcher.device.messages.payload.sensor import OnReadIntent
from dispatcher.handlers.base import EventIntentBaseHandler
from dispatcher.handlers.registry import register_action_event
from notifier.enum import RabbitExchange, RabbitRoutingKey
from notifier.message import NotifierMessage
from notifier.factory.router_notifier_factory import router_notifier_factory
from peripherals.models import RfidCard, Peripherals


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_READ,
)
class OnReadEventHandler(EventIntentBaseHandler):
    exchange = RabbitExchange.SENSOR_SERVICE
    routing_key = RabbitRoutingKey.EVENTS

    def get_extra_notification(self, message: CommandMessage) -> list[NotifierMessage]:
        device = message.device
        access = self._is_card_allowed(message.peripheral, message.payload)
        return [
            router_notifier_factory.device_message(
                router_mac=device.get_router_mac(),
                message=rfid_message_builder.on_read_card_result(message, access),
            ),
        ]

    def _is_card_allowed(self, peripheral: Peripherals, payload: OnReadIntent) -> bool:
        uid = payload.uid
        peripheral = peripheral
        card = RfidCard.objects.filter(
            allowed_peripherals=peripheral, uid=uid, is_active=True
        )
        if not card.exists():
            return False

        card = card.first()
        card.last_used = datetime.now()

        return True
