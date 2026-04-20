import pytest
from aquarium.models import Aquarium
from consumers.router_message.message_type import MessageType

from dispatcher.device.messages.device_message import DeviceMessage
from dispatcher.device.messages.enum import MessageCommand
from dispatcher.handlers.cpu.events.device_connect import DeviceConnectEvent


@pytest.mark.django_db
class TestDeviceConnectEvent:
    def setup_method(self):
        self.event = DeviceConnectEvent()
        self.message = DeviceMessage(
            type=MessageType.REQUEST,
            command=MessageCommand.DEVICE_CONNECT,
            device_id="00:11:22:34:44:55",
            payload={
                "fun": "aquarium",
                "firmware_version": 1.0,
                "wifi_strength": "-50",
            },
            message_id="12345",
        )

    def test_create_device_should_return_device(self, home):
        result = self.event._create_new_device(
            self.message.device_id, self.message.payload, home
        )
        assert result is not None
        assert type(result) is Aquarium
