from pydantic import BaseModel

from consumers.device.messages.device_message import DeviceMessage
from consumers.device.messages.enum import CameraCommand
from consumers.router.message.enum import RouterMessageType
from consumers.router.message.payload.camera import CameraRouterMessagePayload


class RouterMessage(BaseModel):
    target:RouterMessageType


class DeviceRouterMessage(RouterMessage):
    target: RouterMessageType = RouterMessageType.DEVICE
    payload: DeviceMessage


class CameraRouterMessage(RouterMessage):
    target: RouterMessageType = RouterMessageType.CAMERA
    command:CameraCommand
    payload: CameraRouterMessagePayload