from dispatcher.device.messages.builder.base import BaseMessageBuilder
from dispatcher.device.messages.device_message import DeviceMessage
from dispatcher.command_message.message import CommandMessage
from time import time


class CpuMessageBuilder(BaseMessageBuilder):
    def health_check_response(self, message: CommandMessage) -> DeviceMessage:
        return self._build_response(message, {"timestamp": time()})


cpu_message_builder = CpuMessageBuilder()
