from dispatcher.device.messages.builder.base import BaseMessageBuilder
from dispatcher.device.messages.device_message import DeviceMessage
from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.enum import ActionResult


class ActionEventResultMessageBuilder(BaseMessageBuilder):
    def accept_response(self, message: CommandMessage) -> DeviceMessage:
        return self._build_response(message, {"status": ActionResult.ACCEPTED})

    def reject_response(self, message: CommandMessage) -> DeviceMessage:
        return self._build_response(message, {"status": ActionResult.REJECTED})


action_event_result_builder = ActionEventResultMessageBuilder()
