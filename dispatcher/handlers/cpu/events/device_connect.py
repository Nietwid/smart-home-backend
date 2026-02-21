from datetime import datetime

from consumers.frontend_message.frontend_message import FrontendMessage
from consumers.frontend_message.frontend_message_type import FrontendMessageType
from consumers.frontend_message.messenger import FrontendMessenger
from consumers.router_message.builders.basic import basic_response
from consumers.router_message.messenger import DeviceMessenger
from consumers.router_message.payload.basic import DeviceConnectRequest
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer
from dispatcher.base import ActionEventBaseHandler
from dispatcher.command_message import CommandMessage
from room.serializer import RoomSerializer

from device.models import Device


class DeviceConnectEvent(ActionEventBaseHandler):
    """Handles device connection events by updating or creating device records."""

    def __call__(self, message: CommandMessage) -> None:
        device = message.device
        payload: DeviceConnectRequest = message.payload

        device.last_seen = datetime.now()
        device.is_online = True
        device.pending = []
        device.firmware_version = payload.firmware_version
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
