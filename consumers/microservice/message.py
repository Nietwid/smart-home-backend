from datetime import datetime
from pydantic import BaseModel, Field

from dispatcher.device.messages.enum import MessageCommand
from django.utils import timezone


class MicroserviceMessage(BaseModel):
    message_event: MessageCommand
    device_id: str
    peripheral_id: int
    home_id: int
    payload: dict
    timestamp: datetime = Field(default_factory=timezone.localtime)
