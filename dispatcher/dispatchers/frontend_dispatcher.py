from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.message_event import MessageEvent
from dispatcher.base import FrontendBaseHandler
from dispatcher.enums import Scope, MessageType, MessageDirection
from dispatcher.messages.frontend_message import FrontendActionMessage
from dispatcher.registries.frontend_registry import FRONTEND_DISPATCH_TABLE


class FrontendDispatcher:
    def __init__(
        self,
        registry: dict[
            tuple[Scope, MessageType, MessageDirection, MessageEvent],
            FrontendBaseHandler,
        ],
    ):
        self.repository = registry

    def dispatch(self, message: FrontendActionMessage, context) -> None:
        key = (
            message.scope,
            message.message_type,
            message.direction,
            message.message_event,
        )
        handler = self.repository[key]
        handler(message, context)


frontend_dispatcher = FrontendDispatcher(FRONTEND_DISPATCH_TABLE)
