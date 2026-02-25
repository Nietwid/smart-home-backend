import pytest

from consumers.device.messages.enum import MessageEvent
from consumers.router_message.payload.basic import DeviceConnectRequest
from device.models import ChipType
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.enums import Scope, MessageType, MessageDirection


@pytest.fixture
def command_message_device_connect(home, routr, device):
    return CommandMessage(
        scope=Scope.CPU,
        type=MessageType.EVENT,
        direction=MessageDirection.INTENT,
        command=MessageEvent.DEVICE_CONNECT,
        home_id=home.pk,
        router_mac=routr.mac,
        payload=DeviceConnectRequest(
            chip_type=ChipType.ESP32, wifi_strength=-20, firmware_version=1.1
        ),
        message_id="jkdsbfds7218728dsaoundsa98",
        device=device,
    )
