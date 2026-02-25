from consumers.device.messages.message import DeviceMessage
from consumers.router_message.message_event import MessageEvent
from dispatcher.enums import Scope
from dispatcher.command_message.message import CommandMessage
from peripherals.repository import peripheral_repository
from device.repository.device_repository import device_repository


class CommandMessageFactory:

    def resolve(
        self, message: DeviceMessage, home_id: int, router_mac: str
    ) -> CommandMessage:
        """
        Builds a CommandMessage from a raw DeviceMessage.

        Resolves and attaches related domain entities (Device or Peripheral)
        based on message scope and event type, so handlers receive
        a fully prepared execution context.
        """

        device = None
        peripheral = None

        if message.scope == Scope.CPU:
            if message.command == MessageEvent.DEVICE_CONNECT:
                device = device_repository.get_by_mac_or_create(
                    home_id=home_id,
                    mac=message.device_id,
                    chip_type=message.payload.chip_type,
                )
            else:
                device = device_repository.get_by_mac(mac=message.device_id)
        elif message.scope == Scope.PERIPHERAL:
            peripheral = peripheral_repository.get_by_id_with_device(
                message.peripheral_id
            )

        return CommandMessage(
            scope=message.scope,
            type=message.type,
            direction=message.direction,
            command=message.command,
            payload=message.payload,
            message_id=message.message_id,
            device=device,
            peripheral=peripheral,
            home_id=home_id,
            router_mac=router_mac,
        )


command_message_factory = CommandMessageFactory()
