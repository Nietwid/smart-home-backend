from consumers.device.messages.builder.base import BaseMessageBuilder
from dispatcher.command_message.message import CommandMessage


class MeasurementBuilder(BaseMessageBuilder):
    def measurements_sleeping_time_response(self, message: CommandMessage, time: float):
        return self._build_response(message, {"waiting_time": time})
