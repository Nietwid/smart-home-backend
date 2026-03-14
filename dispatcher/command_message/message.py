from typing import Optional, Any
from uuid import uuid4
from pydantic import BaseModel, Field, ConfigDict

from dispatcher.device.messages.enum import MessageCommand
from device.models import Device
from dispatcher.device.messages.enum import MessageType, Scope, MessageDirection
from peripherals.models import Peripherals


def get_message_id():
    return uuid4().hex


class CommandMessage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    scope: Scope
    type: MessageType
    direction: MessageDirection
    command: MessageCommand
    home_id: int
    router_mac: str
    message_id: str = Field(default_factory=get_message_id)
    payload: Any
    device: Optional[Device] = Field(default=None)
    peripheral: Optional[Peripherals] = Field(default=None)
