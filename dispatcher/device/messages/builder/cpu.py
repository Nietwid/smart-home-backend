from django.conf import settings

from dispatcher.device.messages.builder.base import BaseMessageBuilder
from dispatcher.device.messages.device_message import DeviceMessage
from dispatcher.command_message.message import CommandMessage


class CpuMessageBuilder(BaseMessageBuilder):
    def update_peripheral_intent(
        self, message: CommandMessage, data: dict
    ) -> DeviceMessage:
        return self._build_request(message, data)

    def update_rule_intent(self, message: CommandMessage, data: dict) -> DeviceMessage:
        return self._build_request(message, data)

    def update_firmware_intent(
        self,
        message: CommandMessage,
        token: str,
        firmware_name: str,
        firmware_version: int,
    ) -> DeviceMessage:
        return self._build_request(
            message,
            {
                "url": f"{settings.FIRMWARE_DEVICE_ENDPOINT}?token={token}",
                "version": firmware_version,
                "to_device": firmware_name,
            },
        )


cpu_message_builder = CpuMessageBuilder()
