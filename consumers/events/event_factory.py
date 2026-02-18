from consumers.events.basic_event import BasicEvent
from consumers.events.get_connected_devices import GetConnectedDevices
from consumers.events.get_settings import GetSettings
from consumers.events.on_measure_temp_hum import OnMeasureTempHum
from consumers.events.state_change import StateChange
from consumers.events.update_firmware_error import UpdateFirmwareError
from consumers.router_message.message_event import MessageEvent
from consumers.events.access_denied import AccessDeniedEvent
from consumers.events.access_granted import AccessGrantedEvent
from consumers.events.add_tag import AddTagEvent
from consumers.events.blink import BlinkEvent
from consumers.events.camera_answer_event import CameraAnswerEvent
from hardware.device.events_handlers.device_connect import DeviceConnectEvent
from hardware.device.events_handlers.device_disconnect import DeviceDisconnectEvent
from consumers.events.healt_check import HealthCheckEvent
from consumers.events.on_read import OnReadEvent
from consumers.events.camera_error_event import CameraErrorEvent
from consumers.events.set_settings import SetSettings
from consumers.events.on import OnEvent
from consumers.events.toggle import ToggleEvent


def get_event_handler(event_type: MessageEvent):
    """
    Factory function to get the appropriate event handler based on the event type.

    Args:
        event_type (MessageEvent): The type of the event (e.g., 'DEVICE_CONNECT', 'ON_CLICK').

    Returns:
        Callable: The event handler function for the specified event type.
    """
    handlers = {
        MessageEvent.GET_CONNECTED_DEVICES: GetConnectedDevices(),
        MessageEvent.DEVICE_CONNECT: DeviceConnectEvent(),
        MessageEvent.DEVICE_DISCONNECT: DeviceDisconnectEvent(),
        MessageEvent.HEALTH_CHECK: HealthCheckEvent(),
        MessageEvent.SET_SETTINGS: SetSettings(),
        MessageEvent.GET_SETTINGS: GetSettings(),
        MessageEvent.STATE_CHANGE: StateChange(),
        MessageEvent.UPDATE_FIRMWARE_ERROR: UpdateFirmwareError(),
        # Button
        MessageEvent.ON_CLICK: BasicEvent(),
        MessageEvent.ON_HOLD: BasicEvent(),
        MessageEvent.ON_TOGGLE: BasicEvent(),
        # RFID
        MessageEvent.ON_READ: OnReadEvent(),
        MessageEvent.ADD_TAG: AddTagEvent(),
        MessageEvent.ACCESS_DENIED: AccessDeniedEvent(),
        MessageEvent.ACCESS_GRANTED: AccessGrantedEvent(),
        # Lamp
        MessageEvent.ON: OnEvent(),
        MessageEvent.BLINK: BlinkEvent(),
        MessageEvent.TOGGLE: ToggleEvent(),
        # Camera
        MessageEvent.CAMERA_ANSWER: CameraAnswerEvent(),
        MessageEvent.CAMERA_ERROR: CameraErrorEvent(),
        # Temp/Hum
        MessageEvent.ON_MEASURE_TEMPERATURE: OnMeasureTempHum(),
        MessageEvent.ON_MEASURE_HUMIDITY: OnMeasureTempHum(),
        MessageEvent.ON_MEASUREMENT_TEMP_HUM: OnMeasureTempHum(),
        MessageEvent.ON_TEMPERATURE_ABOVE: BasicEvent(),
        MessageEvent.ON_TEMPERATURE_BELOW: BasicEvent(),
        MessageEvent.ON_HUMIDITY_ABOVE: BasicEvent(),
        MessageEvent.ON_HUMIDITY_BELOW: BasicEvent(),
    }
    handler = handlers.get(event_type, None)
    if handler is None:
        raise ValueError(
            f"No handler found for event type: {event_type} did you forget to add it to the factory?"
        )
    return handler
