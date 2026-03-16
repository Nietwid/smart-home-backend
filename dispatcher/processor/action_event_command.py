from dispatcher.command_message.message import CommandMessage
from dispatcher.dispatcher import action_event_dispatcher
from dispatcher.device.messages.enum import Scope, MessageType
from hardware.cpu.device import CpuHardware
from hardware.registry import HARDWARE_REGISTRY
from notifier.notifier import notifier


def action_event_validator(message: CommandMessage) -> None:
    if message.scope == Scope.PERIPHERAL:
        hardware_cls = HARDWARE_REGISTRY[message.peripheral.name]
    elif message.scope == Scope.CPU:
        hardware_cls = CpuHardware
    else:
        raise ValueError(f"Invalid scope: {message.scope}")

    allowed_commands = (
        hardware_cls.get_available_actions()
        if message.type == MessageType.ACTION
        else hardware_cls.events
    )
    if message.command not in allowed_commands:
        raise ValueError(
            f"Invalid {message.type.name.lower()}: {message.command} allowed: {allowed_commands}"
        )


class ActionEventCommandProcessor:

    def __call__(self, message: CommandMessage) -> None:
        action_event_validator(message)
        result = action_event_dispatcher.dispatch(message)
        notifier.notify(result)


action_event_command_processor = ActionEventCommandProcessor()
