from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.builder.rfid import rfid_message_builder
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
    MessageCommand,
)
from dispatcher.device.messages.payload.rfid import OnReadIntent
from dispatcher.dispatch_result import DispatchResult
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.handlers.registry import register_action_event
from notifier.router_notifier_factory import router_notifier_factory
from peripherals.models import RfidCard


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_READ_SUCCESS,
)
class OnReadSuccessEvent(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        device = message.device
        return DispatchResult(
            commands=device.get_event_request(message.peripheral, MessageCommand.ON_READ_SUCCESS),
        )
