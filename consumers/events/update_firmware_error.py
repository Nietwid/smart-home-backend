from consumers.events.base_event import BaseEventRequest
from consumers.frontend.messages.types import (
    FrontendMessageType,
)
from consumers.frontend.messages.messenger import FrontendMessenger
from consumers.router_message.message_event import MessageEvent
from device.serializers.device import DeviceSerializer


class UpdateFirmwareError(BaseEventRequest):
    def handle_request(self, consumer, message):
        device = self._get_device(message.device_id)
        if not device:
            return
        if MessageEvent.UPDATE_FIRMWARE.value in device.pending:
            device.pending.remove(MessageEvent.UPDATE_FIRMWARE.value)
            device.save(update_fields=["pending"])
        data = DeviceSerializer(device).data
        FrontendMessenger().update_frontend(
            device.home.id,
            data,
            status=200,
            action=FrontendMessageType.UPDATE_FIRMWARE_ERROR,
        )
