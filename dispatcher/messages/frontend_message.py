from pydantic.v1 import BaseModel

from consumers.router_message.message_event import MessageEvent
from dispatcher.enums import Scope, MessageType, MessageDirection


class FrontendActionMessage(BaseModel):
    scope: Scope
    message_type: MessageType
    direction: MessageDirection
    message_event: MessageEvent
    device_id: int
    peripheral_id: int
    payload: dict
