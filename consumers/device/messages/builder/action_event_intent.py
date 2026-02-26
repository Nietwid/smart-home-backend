from consumers.device.messages.builder.base import BaseMessageBuilder
from consumers.device.messages.device_message import DeviceMessage
from dispatcher.command_message.message import CommandMessage


class ActionEventIntentMessageBuilder(BaseMessageBuilder):
    def build_intent(self, message: CommandMessage) -> DeviceMessage:
        return self._build_request(message, message.payload)


action_event_intent_builder = ActionEventIntentMessageBuilder()
