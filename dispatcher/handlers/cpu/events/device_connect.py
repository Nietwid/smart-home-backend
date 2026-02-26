from django.utils import timezone

from consumers.device.messages.builder.action_event_request import (
    action_event_response_builder,
)
from consumers.device.messages.enum import MessageEvent
from consumers.frontend.messages.builder import frontend_message_builder
from consumers.frontend.messages.types import (
    FrontendMessageType,
)
from consumers.router.message.message import DeviceRouterMessage
from consumers.device.messages.payload.basic import DeviceConnectRequest
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer

from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.registry import register_action_event
from dispatcher.dispatch_result import DispatchResult
from dispatcher.handlers.enums import Scope, MessageType, MessageDirection
from notifier.message import RouterNotifierData, FrontendNotifierData
from room.serializer import RoomSerializer

from device.models import Device


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageEvent.DEVICE_CONNECT,
)
class DeviceConnectEvent(ActionEventBaseHandler):
    """Handles device connection events by updating or creating device records."""

    def __call__(self, message: CommandMessage) -> DispatchResult:
        device: Device = message.device
        payload: DeviceConnectRequest = message.payload
        home_id = device.home.id
        notifier_message = []
        device.last_seen = timezone.now()
        device.is_online = True
        device.pending = []
        device.firmware_version = payload.firmware_version
        device.save(
            update_fields=["last_seen", "is_online", "pending", "firmware_version"]
        )
        notifier_message.append(
            RouterNotifierData(
                router_mac=device.get_router_mac(),
                data=DeviceRouterMessage(
                    payload=action_event_response_builder.accept_response(message),
                ),
            )
        )

        if device.room is not None:
            notifier_message.extend(
                [
                    FrontendNotifierData(
                        home_id=home_id,
                        data=frontend_message_builder.build(
                            action=FrontendMessageType.UPDATE_DEVICE,
                            data=DeviceSerializer(device).data,
                        ),
                    ),
                    FrontendNotifierData(
                        home_id=home_id,
                        data=frontend_message_builder.build(
                            action=FrontendMessageType.UPDATE_ROOM,
                            data=RoomSerializer(device.room).data,
                        ),
                    ),
                ]
            )
        notifier_message.append(
            FrontendNotifierData(
                home_id=home_id,
                data=frontend_message_builder.build(
                    action=FrontendMessageType.UPDATE_ROUTER,
                    data=RouterSerializer(device.home.router).data,
                ),
            ),
        )
        return DispatchResult(notifications=notifier_message)
