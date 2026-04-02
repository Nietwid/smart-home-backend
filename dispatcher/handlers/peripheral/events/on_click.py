from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.enum import MessageCommand
from device.models import Device
from dispatcher.handlers.base import ActionEventBaseHandler, EventIntentBaseHandler
from dispatcher.dispatch_result import DispatchResult
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_CLICK,
)
class OnClickEventIntentHandler(EventIntentBaseHandler): ...
