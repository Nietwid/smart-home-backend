from dispatcher.device.messages.builder.base import BaseMessageBuilder
from dispatcher.device.messages.device_message import DeviceMessage
from dispatcher.command_message.message import CommandMessage
from time import time
from django.utils import timezone


class CpuMessageBuilder(BaseMessageBuilder):
    def health_check_response(self, message: CommandMessage) -> DeviceMessage:
        now = timezone.localtime(timezone.now())
        utc_ts = now.timestamp()
        offset = now.utcoffset().total_seconds() if now.utcoffset() else 0
        local_timestamp = int(utc_ts + offset)
        return self._build_response(message, {"timestamp": local_timestamp})

    def update_peripheral_intent(
        self, message: CommandMessage, data: dict
    ) -> DeviceMessage:
        return self._build_request(message, data)

    def update_rule_intent(self, message: CommandMessage, data: dict) -> DeviceMessage:
        return self._build_request(message, data)


cpu_message_builder = CpuMessageBuilder()
