from dispatcher.device.messages.enum import MessageAction, MessageEvent, CameraCommand, MessageCommand
from dispatcher.device.messages.payload.basic import *
from dispatcher.device.messages.payload.button import *
from dispatcher.device.messages.payload.camera import *
from dispatcher.device.messages.payload.lamp import *
from dispatcher.device.messages.payload.measurement import *
from dispatcher.device.messages.payload.rfid import *

PAYLOAD_MAPPING: dict = {
    MessageCommand.DEVICE_CONNECT: (DeviceConnectRequest, BasicResult),
    MessageCommand.DEVICE_DISCONNECT: (DeviceDisconnectRequest, BasicResult),
    MessageCommand.ON_TOGGLE: (SerializerDataResponse, BasicResult),
    MessageCommand.UPDATE_PERIPHERAL: (SerializerDataResponse, BasicResult),
    MessageCommand.TOGGLE: (SerializerDataResponse, ToggleResult),
    MessageEvent.UPDATE_CONFIG: (SerializerDataResponse, BasicResult),
    MessageEvent.GET_CONNECTED_DEVICES: (EmptyRequest, BasicResult),
    MessageEvent.HEALTH_CHECK: (HealthCheckRequest, BasicResult),
    MessageEvent.SET_SETTINGS: (SerializerDataResponse, BasicResult),
    MessageEvent.GET_SETTINGS: (EmptyRequest, SerializerDataResponse),
    MessageEvent.STATE_CHANGE: (StateChangeRequest, BasicResult),
    MessageEvent.UPDATE_FIRMWARE: (SerializerDataResponse, BasicResult),
    MessageEvent.UPDATE_FIRMWARE_ERROR: (FirmwareUpdateErrorRequest, BasicResult),
    MessageEvent.ON_READ: (OnReadRequest, BasicResult),
    MessageEvent.ON_CLICK: (SerializerDataResponse, BasicResult),
    MessageEvent.ON_HOLD: (SerializerDataResponse, BasicResult),
    MessageEvent.ON_MEASURE_TEMPERATURE: (TemperatureRequest, SerializerDataResponse),
    MessageEvent.ON_MEASURE_HUMIDITY: (HumidityRequest, SerializerDataResponse),
    MessageEvent.ON_MEASUREMENT_TEMP_HUM: (TempHumRequest, SerializerDataResponse),
    MessageEvent.ON_TEMPERATURE_ABOVE: (EmptyRequest, EmptyResponse),
    MessageEvent.ON_TEMPERATURE_BELOW: (EmptyRequest, EmptyResponse),
    MessageEvent.ON_HUMIDITY_BELOW: (EmptyRequest, EmptyResponse),
    MessageEvent.ON_HUMIDITY_ABOVE: (EmptyRequest, EmptyResponse),
    MessageAction.ON: (SerializerDataResponse, BasicResult),
    MessageAction.OFF: (SerializerDataResponse, BasicResult),
    MessageAction.BLINK: (SerializerDataResponse, BasicResult),
    MessageAction.ACCESS_GRANTED: (AccessGrantedPayload, BasicResult),
    MessageAction.ACCESS_DENIED: (AccessDeniedPayload, BasicResult),
    MessageAction.ADD_TAG: (SerializerDataResponse, AddTagResponse),
    MessageAction.ON_READ_SUCCESS: (SerializerDataResponse, BasicResult),
    MessageAction.ON_READ_FAILURE: (SerializerDataResponse, BasicResult),
    MessageAction.UPDATE_STATE: (SerializerDataResponse, BasicResult),
    CameraCommand.CAMERA_OFFER: (CameraOfferRequest, BasicResult),
    CameraCommand.CAMERA_ANSWER: (EmptyRequest, CameraAnswerResponse),
    CameraCommand.CAMERA_DISCONNECT: (CameraDisconnectPayload, BasicResult),
    CameraCommand.CAMERA_ERROR: (CameraError, CameraError),
    CameraCommand.CAMERA_STOP: (SerializerDataResponse, BasicResult),
    CameraCommand.CAMERA_START: (SerializerDataResponse, BasicResult),
}
