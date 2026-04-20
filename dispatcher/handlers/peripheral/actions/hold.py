from dispatcher.device.messages.enum import MessageCommand
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


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.HOLD,
)
class HoldActionIntent(ActionIntentBaseHandler): ...


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.RESULT,
    handler_name=MessageCommand.HOLD,
)
class HoldActionResult(ActionResultBaseHandler): ...
