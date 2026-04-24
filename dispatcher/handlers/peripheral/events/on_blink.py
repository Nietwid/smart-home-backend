from device.models import Device
from dispatcher.device.messages.enum import MessageCommand
from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.payload.lamp import OnBlinkPayload, OnBlinkStatus
from dispatcher.handlers.base import EventIntentBaseHandler
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
)
from dispatcher.handlers.registry import register_action_event
from notifier.enum import RabbitExchange, RabbitRoutingKey
from notifier.factory.frontend_notifier_factory import frontend_notifier_factory
from notifier.message import NotifierMessage
from peripherals.models import Peripherals
from redis_cache import redis_cache


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_BLINK,
)
class OnBlinkEventIntentHandler(EventIntentBaseHandler):
    exchange = RabbitExchange.SENSOR_SERVICE
    routing_key = RabbitRoutingKey.EVENTS

    def process_message(self, message: CommandMessage) -> None:
        peripheral: Peripherals = message.peripheral
        payload: OnBlinkPayload = message.payload
        if payload.status == OnBlinkStatus.START:
            redis_cache.add_peripheral_pending(
                peripheral.pk, message.command, timeout=90
            )
        elif payload.status == OnBlinkStatus.STOP:
            redis_cache.delete_peripheral_pending(peripheral.pk, message.command)
        else:
            raise ValueError(f"Invalid status: {payload.status}")

    def get_extra_notification(self, message: CommandMessage) -> list[NotifierMessage]:
        device: Device = message.device
        peripheral: Peripherals = message.peripheral
        home_id = device.home.pk
        pending = redis_cache.get_peripherals_pending(peripheral.pk)
        return [
            frontend_notifier_factory.update_peripheral_pending(
                home_id=home_id,
                pending=pending,
                device_id=device.pk,
                peripheral_id=peripheral.pk,
            ),
        ]
