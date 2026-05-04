from dispatcher.device.messages.enum import MessageAction, MessageEvent, CameraCommand, MessageCommand
from dispatcher.device.messages.payload.basic import *
from dispatcher.device.messages.payload.button import *
from dispatcher.device.messages.payload.camera import *
from dispatcher.device.messages.payload.cpu import StartSyncPayload
from dispatcher.device.messages.payload.lamp import *
from dispatcher.device.messages.payload.measurement import *
from dispatcher.device.messages.payload.sensor import *

PAYLOAD_MAPPING: dict = {
    # CPU events
    MessageCommand.DEVICE_CONNECT: (DeviceConnectRequest, BasicResult),
    MessageCommand.DEVICE_DISCONNECT: (DeviceDisconnectRequest, BasicResult),
    MessageCommand.UPDATE_FIRMWARE_ERROR: (FirmwareUpdateErrorRequest, BasicResult),

    # CPU action
    MessageCommand.GET_CONNECTED_DEVICES: (EmptyRequest, BasicResult),
    MessageCommand.UPDATE_PERIPHERAL: (SerializerDataResponse, BasicResult),
    MessageCommand.UPDATE_RULE: (SerializerDataResponse, BasicResult),
    MessageCommand.SYNC_START: (StartSyncPayload, BasicResult),
    MessageCommand.SYNC_END: (StartSyncPayload, BasicResult),
    MessageCommand.RESTART: (SerializerDataResponse, BasicResult),
    MessageCommand.UPDATE_FIRMWARE: (SerializerDataResponse, BasicResult),

    # Peripheral events
    MessageCommand.ON_SYNC_TIME:(EmptyRequest, OnSyncTimeResult),
    MessageCommand.ON_ON:(EmptyRequest, BasicResult),
    MessageCommand.ON_OFF:(EmptyRequest, BasicResult),
    MessageCommand.ON_BLINK:(OnBlinkPayload, BasicResult),
    MessageCommand.ON_READ: (OnReadIntent, BasicResult),
    MessageCommand.ON_UPDATE_STATE: (SerializerDataResponse, BasicResult),
    MessageCommand.ON_MEASURE_TEMPERATURE: (MeasurementIntent, BasicResult),
    MessageCommand.ON_MEASURE_HUMIDITY: (MeasurementIntent, BasicResult),
    MessageCommand.ON_CLICK: (SerializerDataResponse, BasicResult),
    MessageCommand.ON_HOLD: (SerializerDataResponse, BasicResult),
    MessageCommand.ON_READ_SUCCESS: (SerializerDataResponse, BasicResult),
    MessageCommand.ON_READ_FAILURE: (SerializerDataResponse, BasicResult),
    MessageCommand.ON_MOTION: (OnMotionIntent, BasicResult),

    # Peripheral action
    MessageCommand.TOGGLE: (SerializerDataResponse, BasicResult),
    MessageCommand.UPDATE_STATE: (SerializerDataResponse, BasicResult),
    MessageCommand.BLINK: (SerializerDataResponse, BasicResult),
    MessageCommand.ADD_TAG: (AddTagIntent, AddTagResult),
    MessageCommand.PLAY_SEQUENCE: (SerializerDataResponse, AddTagResult),
    MessageCommand.ON: (SerializerDataResponse, BasicResult),
    MessageCommand.OFF: (SerializerDataResponse, BasicResult),
    MessageCommand.ACCESS_GRANTED: (AccessGrantedPayload, BasicResult),
    MessageCommand.ACCESS_DENIED: (AccessDeniedPayload, BasicResult),
    MessageCommand.CLICK: (SerializerDataResponse, BasicResult),
    MessageCommand.HOLD: (SerializerDataResponse, BasicResult),

    MessageEvent.UPDATE_CONFIG: (SerializerDataResponse, BasicResult),
    MessageEvent.SET_SETTINGS: (SerializerDataResponse, BasicResult),
    MessageEvent.GET_SETTINGS: (EmptyRequest, SerializerDataResponse),
    CameraCommand.CAMERA_OFFER: (CameraOfferRequest, BasicResult),
    CameraCommand.CAMERA_ANSWER: (EmptyRequest, CameraAnswerResponse),
    CameraCommand.CAMERA_DISCONNECT: (CameraDisconnectPayload, BasicResult),
    CameraCommand.CAMERA_ERROR: (CameraError, CameraError),
    CameraCommand.CAMERA_STOP: (SerializerDataResponse, BasicResult),
    CameraCommand.CAMERA_START: (SerializerDataResponse, BasicResult),
}
