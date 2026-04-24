from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from dispatcher.device.messages.enum import MessageCommand
from django.utils import timezone


def generate_random_id():
    return uuid4()


class MicroserviceMessage(BaseModel):
    message_id: UUID = Field(default_factory=generate_random_id)
    message_event: MessageCommand
    device_id: str
    peripheral_id: int
    home_id: int
    payload: dict
    timestamp: datetime = Field(default_factory=timezone.localtime)
