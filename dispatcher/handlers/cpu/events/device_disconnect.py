from datetime import datetime

from consumers.frontend.messages.message import FrontendMessage
from consumers.frontend.messages.types import (
    FrontendMessageType,
)
from consumers.frontend.messages.messenger import FrontendMessenger
from device.models import Device
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer
from dispatcher.base import ActionEventBaseHandler
from dispatcher.command_message import CommandMessage
from dispatcher.dispatch_result import DispatchResult
from notifier.message import FrontendNotifierData, NotifierMessage
from room.serializer import RoomSerializer


class DeviceDisconnectEvent(ActionEventBaseHandler):
    """
    Event triggered when a device disconnects.
    """

    def __call__(self, message: CommandMessage) -> DispatchResult:
        device: Device = message.device
        device.last_seen = datetime.now()
        device.is_online = False
        device.pending = []
        device.save(update_fields=["last_seen", "is_online", "pending"])
        home_id = device.home.id
        return DispatchResult(
            notifications=[
                FrontendNotifierData(
                    home_id=home_id,
                    data=FrontendMessage(
                        action=FrontendMessageType.UPDATE_DEVICE,
                        data=DeviceSerializer(device).data,
                    ),
                ),
                FrontendNotifierData(
                    home_id=home_id,
                    data=FrontendMessage(
                        action=FrontendMessageType.UPDATE_ROOM,
                        data=RoomSerializer(device.room).data,
                    ),
                ),
                FrontendNotifierData(
                    home_id=home_id,
                    data=FrontendMessage(
                        action=FrontendMessageType.UPDATE_ROUTER,
                        data=RouterSerializer(device.home.router).data,
                    ),
                ),
            ]
        )
