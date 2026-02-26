from consumers.device.messages.device_message import DeviceMessage
from consumers.frontend.messages.messenger import FrontendMessenger
from consumers.events.base_event import BaseEventResponse
from device.serializers.device import DeviceSerializer


class SetSettings(BaseEventResponse):
    """Handles the response for setting device settings."""

    def handle_request(self, consumer, message: DeviceMessage):
        print(message)

    def handle_response(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            return
        FrontendMessenger().update_frontend(
            device.home.id, DeviceSerializer(device).data
        )
