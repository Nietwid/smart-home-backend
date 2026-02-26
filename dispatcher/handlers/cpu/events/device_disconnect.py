from datetime import datetime

from consumers.device.messages.enum import MessageEvent
from consumers.frontend.messages.message import FrontendMessage
from consumers.frontend.messages.types import (
    FrontendMessageType,
)
from device.models import Device
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.dispatch_result import DispatchResult
from dispatcher.handlers.enums import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from notifier.message import FrontendNotifierData
from room.serializer import RoomSerializer


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageEvent.DEVICE_DISCONNECT,
)
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
