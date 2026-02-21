from typing import Optional, Any

from pydantic import BaseModel, Field

from consumers.router_message.message_event import MessageEvent
from device.models import Device
from dispatcher.enums import MessageType, Scope, MessageDirection
from peripherals.models import Peripherals


class CommandMessage(BaseModel):
    scope: Scope
    type: MessageType
    direction: MessageDirection
    event: MessageEvent
    home_id: int
    router_mac: str
    payload: Any
    message_id: Optional[str] = Field(default=None)
    device: Optional[Device] = Field(default=None)
    peripheral: Optional[Peripherals] = Field(default=None)
