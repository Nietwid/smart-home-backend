from uuid import uuid4

from consumers.router_message.message_event import MessageEvent
from consumers.router_message.message_type import MessageType
from device_consumer.device_message import DeviceMessage


def build_request(event: MessageEvent, device_id: str, payload: dict) -> DeviceMessage:
    return DeviceMessage(
        message_type=MessageType.REQUEST,
        message_event=event,
        device_id=device_id,
        message_id=str(uuid4()),
        payload=payload,
    )


def build_response(request: DeviceMessage, payload: dict) -> DeviceMessage:
    return DeviceMessage(
        message_type=MessageType.RESPONSE,
        message_event=request.message_event,
        device_id=request.device_id,
        message_id=request.message_id,
        payload=payload,
    )
