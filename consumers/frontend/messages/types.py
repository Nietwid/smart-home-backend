from enum import Enum


class FrontendMessageType(Enum):
    UPDATE_PERIPHERAL_STATE = "update_peripheral_state"
    UPDATE_PERIPHERAL_PENDING = "update_peripheral_pending"
    UPDATE_DEVICE_PENDING = "update_device_pending"
    UPDATE_DEVICE_REQUIRED_ACTION = "update_device_required_action"
    DISPLAY_TOASTER = "display_toaster"
    ADD_TAG_RESULT = "add_tag_result"

    UPDATE_ROUTER = "update_router"
    UPDATE_DEVICE = "update_device"
    NEW_DEVICE_CONNECTED = "new_device_connected"
    CAMERA_OFFER = "camera_offer"
    UPDATE_ROOM = "update_room"
    UPDATE_FIRMWARE_ERROR = "update_firmware_error"
    AI_RESPONSE = "ai_response"


