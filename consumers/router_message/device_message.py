import re
from typing import Any, Union
from pydantic import BaseModel, field_validator, model_validator, ValidationError
from .message_event import MessageEvent
from .message_type import MessageType
from consumers.router_message.payload.basic import SerializerDataResponse
from consumers.router_message.payload.payload_mapper import PAYLOAD_MAPPING


class DeviceMessage(BaseModel):
    message_type: MessageType
    message_event: MessageEvent
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
        payload_type = PAYLOAD_MAPPING.get(self.message_event, None)
        if payload_type is None:
            raise ValueError(
                f"Unsupported payload type. Did you forget to register {self.message_event}?",
            )
        model = (
            payload_type[0]
            if self.message_type == MessageType.REQUEST
            else payload_type[1]
        )
        if model is SerializerDataResponse and isinstance(self.payload, dict):
            return self
        self.payload = model(**self.payload)
        return self
