from consumers.router_message.message_event import MessageEvent
from hardware.device.events_handlers.device_disconnect import DeviceDisconnectEvent
from hardware.device.events_handlers.device_connect import DeviceConnectEvent


class DeviceHardware:
    actions = {}
    events = {
        MessageEvent.DEVICE_CONNECT: DeviceConnectEvent,
        MessageEvent.DEVICE_DISCONNECT: DeviceDisconnectEvent,
    }
