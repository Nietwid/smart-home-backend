from consumers.router_message.builders.base import build_request
from consumers.router_message.message_event import MessageEvent


def add_tag_request(mac: str, name: str):
    return build_request(MessageEvent.ADD_TAG, mac, {"name": name})
