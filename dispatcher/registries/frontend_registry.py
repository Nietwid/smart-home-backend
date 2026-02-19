from consumers.router_message.message_event import MessageEvent
from dispatcher.enums import Scope, MessageType, MessageDirection

FRONTEND_DISPATCH_TABLE = {}


def register_device_handler(
    scope: Scope,
    message_type: MessageType,
    direction: MessageDirection,
    handler_name: MessageEvent,
):
    def decorator(cls):
        instance = cls()
        key = (scope, message_type, direction, handler_name)
        if key in FRONTEND_DISPATCH_TABLE:
            raise RuntimeError(f"Handler already registered for {key}")

        FRONTEND_DISPATCH_TABLE[(scope, message_type, direction, handler_name)] = (
            instance
        )
        return cls

    return decorator
