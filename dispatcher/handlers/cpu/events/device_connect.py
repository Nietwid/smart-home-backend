from django.utils import timezone

from dispatcher.device.messages.builder.action_event_request import (
    action_event_result_builder,
)
from dispatcher.device.messages.enum import MessageCommand
from dispatcher.device.messages.payload.basic import DeviceConnectRequest
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer

from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.registry import register_action_event
from dispatcher.dispatch_result import DispatchResult
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.router_notifier_factory import router_notifier_factory
from room.serializer import RoomSerializer

from device.models import Device


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.DEVICE_CONNECT,
)
class DeviceConnectEvent(ActionEventBaseHandler):
    """Handles device connection events by updating or creating device records."""

    def __call__(self, message: CommandMessage) -> DispatchResult:
        device: Device = message.device
        payload: DeviceConnectRequest = message.payload
        home_id = device.home.id
        device.last_seen = timezone.now()
        device.is_online = True
        device.firmware_version = payload.firmware_version
        device.wifi_strength = payload.wifi_strength
        device.save(
            update_fields=[
                "last_seen",
                "is_online",
                "firmware_version",
                "wifi_strength",
            ]
        )

        notifier_message = [
            router_notifier_factory.device_message(
                router_mac=device.get_router_mac(),
                message=action_event_result_builder.accept_response(message),
            ),
            frontend_notifier_factory.update_device(
                home_id=home_id, data=DeviceSerializer(device).data
            ),
            frontend_notifier_factory.update_router(
                home_id=home_id,
                data=RouterSerializer(device.home.router).data,
            ),
        ]

        if device.room is not None:
            notifier_message.append(
                frontend_notifier_factory.update_room(
                    home_id=home_id, data=RoomSerializer(device.room).data
                )
            )
        return DispatchResult(notifications=notifier_message)
