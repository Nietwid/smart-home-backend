from consumers.device.messages.message import DeviceMessage
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.enums import MessageDirection
from time import time


class DeviceMessageBuilder:

    def accept_response(self, message: CommandMessage) -> DeviceMessage:
        return self._build_response(message, {"status": "accepted"})

    def reject_response(self, message: CommandMessage) -> DeviceMessage:
        return self._build_response(message, {"status": "rejected"})

    def health_check_response(self, message: CommandMessage) -> DeviceMessage:
        return self._build_response(message, {"timestamp": time()})

    def _build_response(self, message: CommandMessage, payload: dict) -> DeviceMessage:
        peripheral_id = message.peripheral.pk if message.peripheral else 0
        return DeviceMessage(
            direction=MessageDirection.RESULT,
            command=message.command,
            type=message.type,
            scope=message.scope,
            device_id=message.device.mac,
            peripheral_id=peripheral_id,
            message_id=message.message_id,
            payload=payload,
        )


device_message_builder = DeviceMessageBuilder()
