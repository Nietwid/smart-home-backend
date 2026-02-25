from dispatcher.handlers.enums import Scope, MessageType, MessageDirection
from consumers.device.messages.enum import MessageCommand

DISPATCH_DICT = {}


def register_action_event(
    scope: Scope,
    message_type: MessageType,
    direction: MessageDirection,
    handler_name: MessageCommand,
):
    def wrapper(cls):
        instance = cls()
        key = (scope, message_type, direction, handler_name)
        if key in DISPATCH_DICT:
            raise RuntimeError(f"Handler already registered for {key}")
        DISPATCH_DICT[(scope, message_type, direction, handler_name)] = instance
        return cls

    return wrapper
