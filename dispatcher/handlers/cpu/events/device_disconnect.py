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
from notifier.frontend_notifier_factory import frontend_notifier_factory
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
        device.save(update_fields=["last_seen", "is_online"])
        home_id = device.home.id
        return DispatchResult(
            notifications=[
                frontend_notifier_factory.update_device(
                    home_id=home_id, data=DeviceSerializer(device).data
                ),
                frontend_notifier_factory.update_room(
                    home_id=home_id, data=RoomSerializer(device.room).data
                ),
                frontend_notifier_factory.update_router(
                    home_id=home_id, data=RouterSerializer(device.home.router).data
                ),
            ]
        )
