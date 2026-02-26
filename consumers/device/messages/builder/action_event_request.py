from consumers.device.messages.builder.base import BaseMessageBuilder
from consumers.device.messages.device_message import DeviceMessage
from dispatcher.command_message.message import CommandMessage


class ActionEventResponseMessageBuilder(BaseMessageBuilder):
    def accept_response(self, message: CommandMessage) -> DeviceMessage:
        return self._build_response(message, {"status": "accepted"})

    def reject_response(self, message: CommandMessage) -> DeviceMessage:
        return self._build_response(message, {"status": "rejected"})


action_event_response_builder = ActionEventResponseMessageBuilder()
