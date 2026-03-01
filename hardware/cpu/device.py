from consumers.device.messages.enum import MessageCommand


class CpuHardware:
    actions = (MessageCommand.UPDATE_PERIPHERAL,)
    events = (
        MessageCommand.DEVICE_CONNECT,
        MessageCommand.DEVICE_DISCONNECT,
    )
