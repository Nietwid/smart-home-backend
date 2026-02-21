from typing import Optional, Type

from pydantic import BaseModel, Field

from consumers.router_message.message_event import MessageEvent
from device.models import Device
from dispatcher.enums import MessageType, Scope, MessageDirection
from peripherals.models import Peripherals


class CommandMessage(BaseModel):
    scope: Scope
    message_type: MessageType
    direction: MessageDirection
    message_event: MessageEvent
    home_id: int
    router_mac: str
    payload: Type[BaseModel]
    message_id: Optional[str] = Field(default=None)
    device: Optional[Device] = Field(default=None)
    peripheral: Optional[Peripherals] = Field(default=None)
