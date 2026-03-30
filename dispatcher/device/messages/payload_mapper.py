from dispatcher.device.messages.enum import MessageAction, MessageEvent, CameraCommand, MessageCommand
from dispatcher.device.messages.payload.basic import *
from dispatcher.device.messages.payload.button import *
from dispatcher.device.messages.payload.camera import *
from dispatcher.device.messages.payload.cpu import StartSyncPayload
from dispatcher.device.messages.payload.lamp import *
from dispatcher.device.messages.payload.measurement import *
from dispatcher.device.messages.payload.rfid import *

PAYLOAD_MAPPING: dict = {
    # CPU events
    MessageCommand.DEVICE_CONNECT: (DeviceConnectRequest, BasicResult),
    MessageCommand.DEVICE_DISCONNECT: (DeviceDisconnectRequest, BasicResult),

    # CPU action
    MessageCommand.UPDATE_PERIPHERAL: (SerializerDataResponse, BasicResult),
    MessageCommand.UPDATE_RULE: (SerializerDataResponse, BasicResult),
    MessageCommand.SYNC_START: (StartSyncPayload, BasicResult),
    MessageCommand.SYNC_END: (StartSyncPayload, BasicResult),
    MessageCommand.RESTART: (SerializerDataResponse, BasicResult),

    # Peripheral events
    MessageCommand.ON_TOGGLE: (SerializerDataResponse, ToggleResult),
    MessageCommand.ON_SYNC_TIME:(EmptyRequest, OnSyncTimeResult),
    MessageCommand.ON_BLINK:(OnBlinkPayload, BasicResult),
    MessageCommand.ON_READ: (OnReadIntent, BasicResult),

    # Peripheral action
    MessageCommand.TOGGLE: (SerializerDataResponse, ToggleResult),
    MessageCommand.UPDATE_STATE: (SerializerDataResponse, BasicResult),
    MessageCommand.BLINK: (SerializerDataResponse, BasicResult),
    MessageCommand.ADD_TAG: (AddTagIntent, AddTagResult),

    MessageEvent.UPDATE_CONFIG: (SerializerDataResponse, BasicResult),
    MessageEvent.GET_CONNECTED_DEVICES: (EmptyRequest, BasicResult),
    MessageEvent.SET_SETTINGS: (SerializerDataResponse, BasicResult),
    MessageEvent.GET_SETTINGS: (EmptyRequest, SerializerDataResponse),
    MessageEvent.UPDATE_FIRMWARE: (SerializerDataResponse, BasicResult),
    MessageEvent.UPDATE_FIRMWARE_ERROR: (FirmwareUpdateErrorRequest, BasicResult),
    MessageCommand.ON_CLICK: (SerializerDataResponse, BasicResult),
    MessageCommand.ON_HOLD: (SerializerDataResponse, BasicResult),
    MessageEvent.ON_MEASURE_TEMPERATURE: (TemperatureRequest, SerializerDataResponse),
    MessageEvent.ON_MEASURE_HUMIDITY: (HumidityRequest, SerializerDataResponse),
    MessageEvent.ON_MEASUREMENT_TEMP_HUM: (TempHumRequest, SerializerDataResponse),
    MessageEvent.ON_TEMPERATURE_ABOVE: (EmptyRequest, EmptyResponse),
    MessageEvent.ON_TEMPERATURE_BELOW: (EmptyRequest, EmptyResponse),
    MessageEvent.ON_HUMIDITY_BELOW: (EmptyRequest, EmptyResponse),
    MessageEvent.ON_HUMIDITY_ABOVE: (EmptyRequest, EmptyResponse),
    MessageCommand.ON: (SerializerDataResponse, BasicResult),
    MessageCommand.OFF: (SerializerDataResponse, BasicResult),
    MessageCommand.ACCESS_GRANTED: (AccessGrantedPayload, BasicResult),
    MessageCommand.ACCESS_DENIED: (AccessDeniedPayload, BasicResult),
    MessageCommand.ON_READ_SUCCESS: (SerializerDataResponse, BasicResult),
    MessageCommand.ON_READ_FAILURE: (SerializerDataResponse, BasicResult),
    CameraCommand.CAMERA_OFFER: (CameraOfferRequest, BasicResult),
    CameraCommand.CAMERA_ANSWER: (EmptyRequest, CameraAnswerResponse),
    CameraCommand.CAMERA_DISCONNECT: (CameraDisconnectPayload, BasicResult),
    CameraCommand.CAMERA_ERROR: (CameraError, CameraError),
    CameraCommand.CAMERA_STOP: (SerializerDataResponse, BasicResult),
    CameraCommand.CAMERA_START: (SerializerDataResponse, BasicResult),
}
