from consumers.router_message.message_event import MessageEvent
from dispatcher.base import DeviceBaseHandler
from dispatcher.enums import Scope, MessageType, MessageDirection
from dispatcher.messages.device_message import DeviceMessage
from dispatcher.registries.device_registry import DEVICE_DISPATCH_DICT


class DeviceDispatcher:
    def __init__(
        self,
        registry: dict[
            tuple[Scope, MessageType, MessageDirection, MessageEvent], DeviceBaseHandler
        ],
    ):
        self.repository = registry

    def dispatch(self, message: DeviceMessage, context) -> None:
        key = (
            message.scope,
            message.message_type,
            message.direction,
            message.message_event,
        )
        handler = self.repository[key]
        handler(message, context)


device_dispatcher = DeviceDispatcher(DEVICE_DISPATCH_DICT)
