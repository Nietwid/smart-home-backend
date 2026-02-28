from consumers.device.messages.enum import MessageAction, MessageEvent


class CpuHardware:
    actions = (MessageAction.UPDATE_PERIPHERAL,)
    events =(
            MessageEvent.DEVICE_CONNECT,
            MessageEvent.DEVICE_DISCONNECT,
        ),
