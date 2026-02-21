from consumers.router_message.message_event import MessageEvent
from dispatcher.enums import Scope, MessageType, MessageDirection

DISPATCH_DICT = {}


def register_device_handler(
    scope: Scope,
    message_type: MessageType,
    direction: MessageDirection,
    handler_name: MessageEvent,
):
    def decorator(cls):
        instance = cls()
        key = (scope, message_type, direction, handler_name)
        if key in DISPATCH_DICT:
            raise RuntimeError(f"Handler already registered for {key}")
        DISPATCH_DICT[(scope, message_type, direction, handler_name)] = instance
        return cls

    return decorator
