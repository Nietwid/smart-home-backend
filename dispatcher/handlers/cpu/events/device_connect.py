from datetime import datetime

from consumers.frontend_message.frontend_message import FrontendMessage
from consumers.frontend_message.frontend_message_type import FrontendMessageType
from consumers.frontend_message.messenger import FrontendMessenger
from consumers.router_message.builders.basic import basic_response
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.messenger import DeviceMessenger
from consumers.router_message.payload.basic import DeviceConnectRequest
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer
from device_registry import DeviceRegistry
from hardware.base import EventHandler, DeviceContext
from room.serializer import RoomSerializer

from user.models import Home
from device.models import Device


class DeviceConnectEvent(EventHandler):
    """Handles device connection events by updating or creating device records."""

    def handle_event(self, message: DeviceMessage, context: DeviceContext) -> None:
        device = context.device
        if not device:
            device = self._create_new_device(
                message.device_id, message.payload, context.home_id
            )
        device.last_seen = datetime.now()
        device.is_online = True
        device.pending = []
        device.firmware_version = message.payload.firmware_version
        device.save(
            update_fields=["last_seen", "is_online", "pending", "firmware_version"]
        )
        response = basic_response(message, "accepted")
        DeviceMessenger().send(consumer.mac, response)
        if not device.home:
            return

        home_id = device.home.id
        if device.room is not None:
            FrontendMessenger().update_frontend(home_id, DeviceSerializer(device).data)
            FrontendMessenger().update_frontend(
                home_id,
                RoomSerializer(device.room).data,
                action=FrontendMessageType.UPDATE_ROOM,
            )
        FrontendMessenger().update_frontend(
            home_id,
            RouterSerializer(device.home.router).data,
            action=FrontendMessageType.UPDATE_ROUTER,
        )

    def _create_new_device(
        self, mac: str, payload: DeviceConnectRequest, home: int
    ) -> Device | None:
        """Creates a new device record based on the message payload."""
        home
        device = Device.objects.create(
            home=home,
            mac=mac,
            wifi_strength=payload.wifi_strength,
            is_online=True,
        )
        message = FrontendMessage(
            action=FrontendMessageType.NEW_DEVICE_CONNECTED,
            data=DeviceSerializer(device).data,
            status=200,
        )
        FrontendMessenger().send(device.home.pk, message)
        return device
