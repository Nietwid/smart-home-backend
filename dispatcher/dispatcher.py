import logging

from consumers.router_message.message_event import MessageEvent
from dispatcher.base import ActionEventBaseHandler
from dispatcher.command_message import CommandMessage
from dispatcher.enums import Scope, MessageType, MessageDirection
from dispatcher.device_registry import DISPATCH_DICT

logger = logging.getLogger(__name__)


class ActionEventDispatcher:
    def __init__(
        self,
        registry: dict[
            tuple[Scope, MessageType, MessageDirection, MessageEvent],
            ActionEventBaseHandler,
        ],
    ):
        self.repository = registry

    def dispatch(self, message: CommandMessage) -> None:
        key = (
            message.scope,
            message.message_type,
            message.direction,
            message.message_event,
        )
        try:
            handler = self.repository[key]
        except KeyError:
            logger.error(f"No handler registered for {key}")
            return
        handler(message)


device_dispatcher = ActionEventDispatcher(DISPATCH_DICT)
