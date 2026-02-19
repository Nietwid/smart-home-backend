import pytest
from aquarium.models import Aquarium
from consumers.router_message.message_event import MessageEvent
from consumers.router_message.message_type import MessageType
from dispatcher.handlers.cpu.events.device_connect import DeviceConnectEvent
from consumers.router_message.device_message import DeviceMessage


@pytest.mark.django_db
class TestDeviceConnectEvent:
    def setup_method(self):
        self.event = DeviceConnectEvent()
        self.message = DeviceMessage(
            message_type=MessageType.REQUEST,
            message_event=MessageEvent.DEVICE_CONNECT,
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
