from dispatcher.device.messages.builder.base import BaseMessageBuilder
from dispatcher.device.messages.device_message import DeviceMessage
from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.enum import ActionResult
from dispatcher.device.messages.payload.basic import BasicResult


class RfidMessageBuilder(BaseMessageBuilder):
    def add_tag_intent(self, message: CommandMessage) -> DeviceMessage:
        return self._build_request(message, message.payload)

    def on_read_card_result(
        self, message: CommandMessage, accept: bool
    ) -> DeviceMessage:
        return self._build_response(
            message,
            BasicResult(
                status=ActionResult.ACCEPTED if accept else ActionResult.REJECTED
            ).model_dump(),
        )


rfid_message_builder = RfidMessageBuilder()
