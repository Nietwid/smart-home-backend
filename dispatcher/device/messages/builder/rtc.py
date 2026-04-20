from dispatcher.device.messages.builder.base import BaseMessageBuilder
from dispatcher.device.messages.device_message import DeviceMessage
from dispatcher.command_message.message import CommandMessage
from django.utils import timezone


class RtcMessageBuilder(BaseMessageBuilder):
    def on_sync_time_result(self, message: CommandMessage) -> DeviceMessage:
        now = timezone.localtime(timezone.now())
        utc_ts = now.timestamp()
        offset = now.utcoffset().total_seconds() if now.utcoffset() else 0
        local_timestamp = int(utc_ts + offset)
        return self._build_response(message, {"timestamp": local_timestamp})


rtc_message_builder = RtcMessageBuilder()
