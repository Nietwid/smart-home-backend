from pydantic import BaseModel, Field
from typing import Literal

from hardware.base import BasePeripheralConfig


class PinOutputConfig(BasePeripheralConfig):
    pin: int = Field(ge=0, le=40)


class PinOutputState(BaseModel):
    is_on: bool = Field(default=False)


class PinInputConfig(BasePeripheralConfig):
    pin: int
    mode: Literal["PULL_UP", "PULL_DOWN", "INPUT"]


class PinInputState(BaseModel):
    is_on: bool = Field(default=False)
