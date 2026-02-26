from consumers.device.messages.enum import MessageAction, MessageEvent
from consumers.device.messages.payload.camera import *
from consumers.device.messages.payload.basic import *
from consumers.device.messages.payload.measurement import *
from consumers.device.messages.payload.rfid import *

PAYLOAD_MAPPING: dict = {
    MessageEvent.UPDATE_CONFIG: (SerializerDataResponse, BasicResponse),
    MessageEvent.GET_CONNECTED_DEVICES: (EmptyRequest, BasicResponse),
    MessageEvent.DEVICE_CONNECT: (DeviceConnectRequest, BasicResponse),
    MessageEvent.DEVICE_DISCONNECT: (DeviceDisconnectRequest, BasicResponse),
    MessageEvent.HEALTH_CHECK: (HealthCheckRequest, BasicResponse),
    MessageEvent.SET_SETTINGS: (SerializerDataResponse, BasicResponse),
    MessageEvent.GET_SETTINGS: (EmptyRequest, SerializerDataResponse),
    MessageEvent.STATE_CHANGE: (StateChangeRequest, BasicResponse),
    MessageEvent.UPDATE_FIRMWARE: (SerializerDataResponse, BasicResponse),
    MessageEvent.UPDATE_FIRMWARE_ERROR: (FirmwareUpdateErrorRequest, BasicResponse),
    MessageAction.ADD_TAG: (SerializerDataResponse, AddTagResponse),
    MessageEvent.ON_READ: (OnReadRequest, BasicResponse),
    MessageAction.ON_READ_SUCCESS: (SerializerDataResponse, BasicResponse),
    MessageAction.ON_READ_FAILURE: (SerializerDataResponse, BasicResponse),
    MessageEvent.ON_CLICK: (SerializerDataResponse, BasicResponse),
    MessageEvent.ON_HOLD: (SerializerDataResponse, BasicResponse),
    MessageEvent.ON_TOGGLE: (SerializerDataResponse, BasicResponse),
    MessageAction.ON: (SerializerDataResponse, BasicResponse),
    MessageAction.OFF: (SerializerDataResponse, BasicResponse),
    MessageAction.BLINK: (SerializerDataResponse, BasicResponse),
    MessageAction.TOGGLE: (SerializerDataResponse, BasicResponse),
    MessageAction.ACCESS_GRANTED: (AccessGrantedPayload, BasicResponse),
    MessageAction.ACCESS_DENIED: (AccessDeniedPayload, BasicResponse),
    MessageEvent.CAMERA_OFFER: (CameraOfferRequest, BasicResponse),
    MessageEvent.CAMERA_ANSWER: (EmptyRequest, CameraAnswerResponse),
    MessageEvent.CAMERA_DISCONNECT: (CameraDisconnectPayload, BasicResponse),
    MessageEvent.CAMERA_ERROR: (CameraError, CameraError),
    MessageEvent.CAMERA_STOP: (SerializerDataResponse, BasicResponse),
    MessageEvent.CAMERA_START: (SerializerDataResponse, BasicResponse),
    MessageEvent.ON_MEASURE_TEMPERATURE: (TemperatureRequest, SerializerDataResponse),
    MessageEvent.ON_MEASURE_HUMIDITY: (HumidityRequest, SerializerDataResponse),
    MessageEvent.ON_MEASUREMENT_TEMP_HUM: (TempHumRequest, SerializerDataResponse),
    MessageEvent.ON_TEMPERATURE_ABOVE: (EmptyRequest, EmptyResponse),
    MessageEvent.ON_TEMPERATURE_BELOW: (EmptyRequest, EmptyResponse),
    MessageEvent.ON_HUMIDITY_BELOW: (EmptyRequest, EmptyResponse),
    MessageEvent.ON_HUMIDITY_ABOVE: (EmptyRequest, EmptyResponse),
}
