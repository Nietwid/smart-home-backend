
from pydantic import BaseModel

from dispatcher.device.messages.enum import ActionResult

from device.models import ChipType

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


class BasicResult(BaseModel):
    status: ActionResult


class DeviceConnectRequest(BaseModel):
    wifi_strength: int
    firmware_version: float
    chip_type: ChipType


class DeviceDisconnectRequest(BaseModel):
    pass


class OnSyncTimeResult(BaseModel):
    timestamp: int


class FirmwareUpdateErrorRequest(BaseModel):
    message: str


class SetSettingsRequest(BaseModel):
    pass


class DeviceDisconnectResponse(BaseModel):
    pass




class SetSettingsResponse(BaseModel):
    pass
