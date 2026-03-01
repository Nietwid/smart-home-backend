from consumers.microservice_message.microservice_message import MicroserviceMessage
from dispatcher.device.messages.device_state import DeviceState
from consumers.router_message.message_event import MessageEvent


def on_state_change(device_id: int, home_id: int, value: DeviceState):
    return MicroserviceMessage(
        message_event=MessageEvent.STATE_CHANGE,
        device_id=device_id,
        home_id=home_id,
        payload={"state": value},
    )
