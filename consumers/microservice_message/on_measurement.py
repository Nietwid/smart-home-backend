from consumers.microservice_message.microservice_message import MicroserviceMessage
from consumers.router_message.message_event import MessageEvent
from utils.round_timestamp_to_nearest_hour import round_timestamp_to_nearest_hour


def on_measurement(event: MessageEvent, sensor_id: int, home_id: int, value: float):
    return MicroserviceMessage(
        message_event=event,
        device_id=sensor_id,
        home_id=home_id,
        payload={
            "timestamp": round_timestamp_to_nearest_hour(),
            "value": value,
        },
    )
