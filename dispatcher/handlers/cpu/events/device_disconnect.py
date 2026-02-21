from datetime import datetime

from consumers.frontend.messages.types import (
    FrontendMessageType,
)
from consumers.frontend.messages.messenger import FrontendMessenger
from consumers.router_message.device_message import DeviceMessage
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer
from hardware.base import EventHandler
from room.serializer import RoomSerializer


class DeviceDisconnectEvent(EventHandler):
    """
    Event triggered when a device disconnects.
    """

    def handle_event(self, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            return
        device.last_seen = datetime.now()
        device.is_online = False
        device.pending = []
        device.save(update_fields=["last_seen", "is_online", "pending"])
        FrontendMessenger().update_frontend(
            device.home.pk, DeviceSerializer(device).data
        )
        FrontendMessenger().update_frontend(
            device.home.id,
            RoomSerializer(device.room).data,
            action=FrontendMessageType.UPDATE_ROOM,
        )
        FrontendMessenger().update_frontend(
            device.home.id,
            RouterSerializer(device.home.router).data,
            action=FrontendMessageType.UPDATE_ROUTER,
        )
