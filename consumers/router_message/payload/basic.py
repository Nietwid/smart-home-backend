from typing import Literal

from pydantic import BaseModel, field_validator

from consumers.router_message.device_state import DeviceState
from device_registry import DeviceRegistry


class EmptyRequest(BaseModel):
    """Used for request events without payload."""

    pass


class EmptyResponse(BaseModel):
    """Used for response events without payload."""

    pass


class SerializerDataResponse(BaseModel):
    """
    Marker class used in PAYLOAD_MAPPING to indicate
    that the payload comes from a DRF serializer and
    should be treated as a raw validated dict.
    """

    pass


class BasicResponse(BaseModel):
    status: Literal["accepted", "rejected"]


class DeviceConnectRequest(BaseModel):
    wifi_strength: int
    firmware_version: float


class DeviceDisconnectRequest(BaseModel):
    pass


class HealthCheckRequest(BaseModel):
    wifi_strength: int


class StateChangeRequest(BaseModel):
    state: DeviceState


class FirmwareUpdateErrorRequest(BaseModel):
    message: str


class SetSettingsRequest(BaseModel):
    pass


class DeviceDisconnectResponse(BaseModel):
    pass


class HealthCheckResponse(BaseModel):
    pass


class SetSettingsResponse(BaseModel):
    pass
