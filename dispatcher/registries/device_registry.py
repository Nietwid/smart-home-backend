from consumers.router_message.message_event import MessageEvent
from dispatcher.enums import Scope, MessageType, MessageDirection

DEVICE_DISPATCH_DICT = {}


def register_device_handler(
    scope: Scope,
    message_type: MessageType,
    direction: MessageDirection,
    handler_name: MessageEvent,
):
    def decorator(cls):
        instance = cls()
        key = (scope, message_type, direction, handler_name)
        if key in DEVICE_DISPATCH_DICT:
            raise RuntimeError(f"Handler already registered for {key}")
        DEVICE_DISPATCH_DICT[(scope, message_type, direction, handler_name)] = instance
        return cls

    return decorator
