from dispatcher.device.messages.enum import MessageEvent, MessageCommand
from device.models import Device
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.dispatch_result import DispatchResult
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from peripherals.models import Peripherals


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_TOGGLE,
)
class OnToggleEventHandler(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        device: Device = message.device
        peripheral: Peripherals = message.peripheral
        return DispatchResult(commands=device.get_event_request(MessageEvent.ON_CLICK))
