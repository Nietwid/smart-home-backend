from django.utils import timezone

from dispatcher.device.messages.builder.action_event_request import (
    action_event_result_builder,
)
from dispatcher.device.messages.enum import MessageCommand
from dispatcher.device.messages.payload.basic import (
    DeviceConnectRequest,
    FirmwareUpdateErrorRequest,
)
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer

from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.registry import register_action_event
from dispatcher.dispatch_result import DispatchResult
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from notifier.factory.frontend_notifier_factory import frontend_notifier_factory
from notifier.factory.router_notifier_factory import router_notifier_factory
from room.serializer import RoomSerializer

from device.models import Device
from redis_cache import redis_cache


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.UPDATE_FIRMWARE_ERROR,
)
class UpdateFirmwareErrorEvent(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        device: Device = message.device
        payload: FirmwareUpdateErrorRequest = message.payload
        redis_cache.delete_device_pending(message.device.mac, message.command)
        home_id = device.home.id
        error_message = f"Unable to update firmware for device {device.name} reason: {payload.message}"
        notifier_message = [
            frontend_notifier_factory.update_device_pending(
                home_id=home_id,
                pending=redis_cache.get_device_pending(device.mac),
                device_id=device.pk,
            ),
            frontend_notifier_factory.display_toaster(
                home_id=home_id, message=error_message
            ),
        ]
        return DispatchResult(notifications=notifier_message)
