from consumers.device.messages.builder.base import BaseMessageBuilder
from consumers.device.messages.device_message import DeviceMessage
from dispatcher.command_message.message import CommandMessage


class RfidMessageBuilder(BaseMessageBuilder):
    def add_tag_request(self, message: CommandMessage) -> DeviceMessage:
        return self._build_request(message, {})
