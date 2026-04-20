from dispatcher.device.messages.enum import MessageCommand
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import (
    ActionIntentBaseHandler,
    ActionResultBaseHandler,
)
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
)
from dispatcher.handlers.registry import register_action_event
from peripherals.serializers.peripheral import PeripheralSerializer


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.UPDATE_STATE,
)
class UpdateStateActionIntent(ActionIntentBaseHandler):
    def validate_payload(self, message: CommandMessage) -> None:
        serializer = PeripheralSerializer(
            data={
                "name": message.peripheral.name,
                "state": message.payload,
                "device": message.peripheral.device.pk,
            },
            partial=True,
        )
        serializer.is_valid(raise_exception=True)


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.RESULT,
    handler_name=MessageCommand.UPDATE_STATE,
)
class UpdateStateActionResult(ActionResultBaseHandler): ...
