from typing import Optional, Any

from pydantic import BaseModel, Field, ConfigDict

from consumers.device.messages.enum import MessageCommand
from device.models import Device
from dispatcher.handlers.enums import MessageType, Scope, MessageDirection
from peripherals.models import Peripherals


class CommandMessage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    scope: Scope
    type: MessageType
    direction: MessageDirection
    command: MessageCommand
    home_id: int
    router_mac: str
    payload: Any
    message_id: Optional[str] = Field(default=None)
    device: Optional[Device] = Field(default=None)
    peripheral: Optional[Peripherals] = Field(default=None)
