from datetime import datetime

from consumers.device.messages.builder import device_message_builder
from consumers.frontend.messages.builder import frontend_message_builder
from consumers.frontend.messages.types import (
    FrontendMessageType,
)
from consumers.router_message.payload.basic import DeviceConnectRequest
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer

from dispatcher.base import ActionEventBaseHandler
from dispatcher.command_message import CommandMessage
from dispatcher.dispatch_result import DispatchResult
from notifier.message import DeviceNotifierData, FrontendNotifierData
from room.serializer import RoomSerializer

from device.models import Device


class DeviceConnectEvent(ActionEventBaseHandler):
    """Handles device connection events by updating or creating device records."""

    def __call__(self, message: CommandMessage) -> DispatchResult:
        device: Device = message.device
        payload: DeviceConnectRequest = message.payload
        home_id = device.home.id
        notifier_message = []
        device.last_seen = datetime.now()
        device.is_online = True
        device.pending = []
        device.firmware_version = payload.firmware_version
        device.save(
            update_fields=["last_seen", "is_online", "pending", "firmware_version"]
        )

        notifier_message.append(
            DeviceNotifierData(
                router_mac=device.get_router_mac(),
                data=device_message_builder.accept_response(message),
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
