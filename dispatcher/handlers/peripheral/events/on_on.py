from dispatcher.device.messages.enum import MessageCommand
from dispatcher.handlers.base import EventIntentBaseHandler
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_ON,
)
class OnOnEventHandler(EventIntentBaseHandler): ...
