from abc import ABC, abstractmethod

from asgiref.sync import async_to_sync

from dispatcher.device.messages.builders import get_event_request
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.message_event import MessageEvent

from device.models import Device


class BaseEvent(ABC):

    def _get_device(self, mac: str) -> Device | None:
        """Retrieve the device by its MAC address."""
        try:
            return Device.objects.get(mac=mac)
        except Device.DoesNotExist:
            return None

    def get_event_request(self, device: Device, event: MessageEvent):
        if device.fun == "light":
            events = device.events.filter(event=event.value).exclude(
                target_device__mac=device.mac
            )
        else:
            events = device.events.filter(event=event.value)
        if not events.exists():
            return []
        return [get_event_request(event) for event in events]

    @async_to_sync
    async def send_actions_request(self, actions: list[DeviceMessage], consumer):
        for action in actions:
            await consumer.router_send(action.model_dump_json())


class BaseEventRequest(BaseEvent):
    """
    Base class for handling device events request.
    This class defines the interface for handling requests from devices.
    """

    @abstractmethod
    def handle_request(self, consumer, message: DeviceMessage):
        """
        Handle the incoming request.
        This method should be implemented by subclasses to process the request.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class BaseEventResponse(BaseEvent):
    """
    Base class for handling device event responses.
    This class defines the interface for handling responses from device.
    """

    @abstractmethod
    def handle_response(self, consumer, message: DeviceMessage):
        """
        Handle the response from the server.
        This method should be implemented by subclasses to process the response.
        """
        raise NotImplementedError("Subclasses must implement this method.")
