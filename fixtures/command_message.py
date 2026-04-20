import pytest

from dispatcher.device.messages.enum import MessageCommand
from dispatcher.device.messages.payload.basic import DeviceConnectRequest
from device.models import ChipType
from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection


@pytest.fixture
def command_message_device_connect(home, router, device):
    return CommandMessage(
        scope=Scope.CPU,
        type=MessageType.EVENT,
        direction=MessageDirection.INTENT,
        command=MessageCommand.DEVICE_CONNECT,
        home_id=home.pk,
        router_mac=router.mac,
        payload=DeviceConnectRequest(
            chip_type=ChipType.ESP32, wifi_strength=-20, firmware_version=1.1
        ),
        message_id="jkdsbfds7218728dsaoundsa98",
        device=device,
    )
