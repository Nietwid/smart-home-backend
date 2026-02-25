import re
from typing import Any

from pydantic import BaseModel, field_validator, model_validator

from consumers.device.messages.enum import MessageAction
from consumers.router_message.message_event import MessageEvent
from consumers.router_message.payload.basic import SerializerDataResponse
from consumers.router_message.payload.payload_mapper import PAYLOAD_MAPPING
from dispatcher.enums import MessageType, MessageDirection, Scope


class DeviceMessage(BaseModel):
    direction: MessageDirection
    command: MessageEvent | MessageAction
    type: MessageType
    scope: Scope
    device_id: str
    peripheral_id: int
    message_id: str
    payload: Any

    @field_validator("device_id", mode="after")
    def validate_mac(cls, value):
        pattern = r"^([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]){2}$"
        if not re.match(pattern, value) and value != "camera":
            raise ValueError("Invalid MAC address")
        return value

    @model_validator(mode="after")
    def validate_payload(self):
        payload_type = PAYLOAD_MAPPING.get(self.command, None)
        if payload_type is None:
            raise ValueError(
                f"Unsupported payload type. Did you forget to register {self.command}?",
            )
        model = (
            payload_type[0]
            if self.direction == MessageDirection.INTENT
            else payload_type[1]
        )
        if isinstance(self.payload, model):
            return self
        if model is SerializerDataResponse and isinstance(self.payload, dict):
            return self
        self.payload = model(**self.payload)
        return self
