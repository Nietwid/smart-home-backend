from uuid import uuid4, UUID
from typing import Annotated, Union, Literal
from pydantic import BaseModel, Field, RootModel, ConfigDict

from dispatcher.device.messages.device_message import DeviceMessage
from dispatcher.device.messages.enum import CameraCommand
from consumers.router.message.enum import RouterMessageType
from consumers.router.message.payload.camera import CameraRouterMessagePayload

def generate_random_id():
    return uuid4()

class RouterMessage(BaseModel):
    target: RouterMessageType
    message_id: UUID = Field(default_factory=generate_random_id)

class DeviceRouterMessage(RouterMessage):
    target: Literal[RouterMessageType.DEVICE] = RouterMessageType.DEVICE
    payload: DeviceMessage

class CameraRouterMessage(RouterMessage):
    target: Literal[RouterMessageType.CAMERA] = RouterMessageType.CAMERA
    command: CameraCommand
    payload: CameraRouterMessagePayload

class AckRouterMessage(RouterMessage):
    target: Literal[RouterMessageType.ACK] = RouterMessageType.ACK

class RouterMessagePacket(RootModel):
    root: Annotated[
        Union[DeviceRouterMessage, CameraRouterMessage, AckRouterMessage],
        Field(discriminator="target"),
    ]
