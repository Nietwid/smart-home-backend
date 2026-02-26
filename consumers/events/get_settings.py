from consumers.events.base_event import BaseEventRequest, BaseEventResponse
from consumers.device.messages.builders import data_response
from consumers.router_message.device_message import DeviceMessage
from consumers.router.messenger import DeviceMessenger
from device_registry import DeviceRegistry


class GetSettings(BaseEventRequest, BaseEventResponse):
    """Handles the response for setting device settings."""

    def handle_request(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            return
        device_registry = DeviceRegistry()
        model = device_registry.get_model(device.fun)
        serializer_device = device_registry.get_serializer_device(device.fun)
        response = data_response(
            message, serializer_device(model.objects.get(pk=device.pk)).data
        )
        DeviceMessenger().send(consumer.mac, response)

    def handle_response(self, consumer, message: DeviceMessage):
        pass
