from consumers.device.messages.device_message import DeviceMessage
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.enums import MessageDirection, Scope


class BaseMessageBuilder:
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

    def _build_request(self, message: CommandMessage, payload: dict) -> DeviceMessage:
        if message.scope == Scope.CPU:
            device_id = message.device.mac
            peripheral_id = 0
        else:
            device_id = message.peripheral.device.mac
            peripheral_id = message.peripheral.pk
        return DeviceMessage(
            direction=MessageDirection.INTENT,
            command=message.command,
            type=message.type,
            scope=message.scope,
            device_id=device_id,
            peripheral_id=peripheral_id,
            payload=payload,
        )
