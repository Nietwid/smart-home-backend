from enum import Enum


class FrontendMessageType(Enum):
    UPDATE_ROUTER = "update_router"
    UPDATE_DEVICE = "update_device"
    NEW_DEVICE_CONNECTED = "new_device_connected"
    CAMERA_OFFER = "camera_offer"
    UPDATE_ROOM = "update_room"
    UPDATE_FIRMWARE_ERROR = "update_firmware_error"
    AI_RESPONSE = "ai_response"
