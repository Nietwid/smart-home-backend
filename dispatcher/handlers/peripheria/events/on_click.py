from consumers.device.messages.enum import MessageEvent
from device.models import Device
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.dispatch_result import DispatchResult
from dispatcher.handlers.enums import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageEvent.ON_CLICK,
)
class OnClickEventIntentHandler(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        """
        Handle the incoming request for a click event.
        """
        device: Device = message.device
        return DispatchResult(commands=device.get_event_request(MessageEvent.ON_CLICK))


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.RESULT,
    handler_name=MessageEvent.ON_CLICK,
)
class OnClickEventResultHandler(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        """
        Handle the response from the device for a click event.
        """
        # Process the response as needed
        return DispatchResult()
