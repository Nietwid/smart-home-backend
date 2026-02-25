import time
from typing import Literal

from consumers.device.messages.message import DeviceMessage
from consumers.router_message.builders.base import build_response, build_request
from consumers.router_message.message_event import MessageEvent
from device.models import Event


def basic_response(
    message: DeviceMessage, status_type: Literal["accepted", "rejected"]
) -> DeviceMessage:
    return build_response(message, {"status": status_type})


def data_response(message: DeviceMessage, data: dict) -> DeviceMessage:
    return build_response(message, data)


def set_settings_request(mac: str, payload: dict) -> DeviceMessage:
    return build_request(MessageEvent.SET_SETTINGS, mac, payload)


def health_check_response(message: DeviceMessage) -> DeviceMessage:
    return build_response(message, {"timestamp": time.time()})


def get_event_request(event: Event):
    return build_request(
        MessageEvent(event.action), event.target_device.mac, event.extra_settings
    )


def get_intent_request(
    intent: MessageEvent, target_device_mac: str, extra_settings: dict = None
):
    return build_request(
        intent,
        target_device_mac,
        extra_settings if extra_settings else {},
    )


def get_connected_devices_request() -> DeviceMessage:
    return build_request(MessageEvent.GET_CONNECTED_DEVICES, "00:00:00:00:00:00", {})


def update_firmware_request(mac: str, payload: dict) -> DeviceMessage:
    return build_request(MessageEvent.UPDATE_FIRMWARE, mac, payload)
