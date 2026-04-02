from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
    MessageCommand,
)
from dispatcher.handlers.base import EventIntentBaseHandler
from dispatcher.handlers.registry import register_action_event


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_READ_FAILURE,
)
class OnReadFailureEvent(EventIntentBaseHandler): ...
