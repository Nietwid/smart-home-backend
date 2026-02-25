from uuid import uuid4

from consumers.device.messages.message import DeviceMessage
from consumers.router_message.message_event import MessageEvent
from consumers.router_message.message_type import MessageType


def build_request(event: MessageEvent, device_id: str, payload: dict) -> DeviceMessage:
    return DeviceMessage(
        type=MessageType.REQUEST,
        command=event,
        device_id=device_id,
        message_id=str(uuid4()),
        payload=payload,
    )


def build_response(request: DeviceMessage, payload: dict) -> DeviceMessage:
    return DeviceMessage(
        type=MessageType.RESPONSE,
        command=request.command,
        device_id=request.device_id,
        message_id=request.message_id,
        payload=payload,
    )
