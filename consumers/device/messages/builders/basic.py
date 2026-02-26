import time
from typing import Literal

from consumers.device.messages.enum import MessageEvent
from consumers.device.messages.device_message import DeviceMessage
from device.models import Event


def data_response(message: DeviceMessage, data: dict) -> DeviceMessage:
    return build_response(message, data)


def set_settings_request(mac: str, payload: dict) -> DeviceMessage:
    return build_request(MessageEvent.SET_SETTINGS, mac, payload)


def get_event_request(event: Event):
    return build_request(
        MessageEvent(event.action), event.target_device.mac, event.extra_settings
    )


def get_connected_devices_request() -> DeviceMessage:
    return build_request(MessageEvent.GET_CONNECTED_DEVICES, "00:00:00:00:00:00", {})


def update_firmware_request(mac: str, payload: dict) -> DeviceMessage:
    return build_request(MessageEvent.UPDATE_FIRMWARE, mac, payload)
