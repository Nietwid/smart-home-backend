from consumers.router_message.builders.base import build_request
from consumers.router_message.message_event import MessageEvent
from dispatcher.messages.device_message import DeviceMessage


def add_tag_request(mac: str, name: str) -> DeviceMessage:
    return build_request(MessageEvent.ADD_TAG, mac, {"name": name})
