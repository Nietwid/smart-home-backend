import pytest

from consumers.device.messages.enum import MessageEvent
from consumers.device.messages.message import DeviceMessage
from consumers.router_message.payload.basic import DeviceConnectRequest
from device.models import ChipType
from dispatcher.handlers.enums import MessageDirection, MessageType, Scope
from .base import device


@pytest.fixture
def device_message_device_connect(device):
    return DeviceMessage(
        direction=MessageDirection.INTENT,
        command=MessageEvent.DEVICE_CONNECT,
        type=MessageType.EVENT,
        scope=Scope.CPU,
        device_id=device.mac,
        peripheral_id=0,
        message_id="1234",
        payload=DeviceConnectRequest(
            chip_type=ChipType.ESP32, wifi_strength=-20, firmware_version=1.1
        ).model_dump(),
    )
