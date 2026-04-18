from typing import Collection
from dispatcher.device.messages.enum import MessageCommand


class CpuHardware:
    actions = (
        MessageCommand.SYNC_START,
        MessageCommand.SYNC_END,
        MessageCommand.RESTART,
        MessageCommand.UPDATE_PERIPHERAL,
        MessageCommand.UPDATE_RULE,
        MessageCommand.UPDATE_FIRMWARE,
    )

    events = (
        MessageCommand.DEVICE_CONNECT,
        MessageCommand.DEVICE_DISCONNECT,
    )

    @classmethod
    def get_available_actions(cls) -> Collection[MessageCommand]:
        return cls.actions
