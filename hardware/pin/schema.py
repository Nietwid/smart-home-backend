from pydantic import BaseModel, Field
from typing import Literal

from hardware.base import BaseHardwareSchema


class PinOutputConfig(BaseHardwareSchema):
    pin: int = Field(
        ...,
        title="GPIO Pin",
        description="Number of the GPIO pin used as output",
        ge=0,
        le=40,
        examples=[13],
    )


class PinOutputState(BaseModel):
    value: bool = Field(default=False)


class PinInputConfig(BaseHardwareSchema):
    pin: int
    mode: Literal["PULL_UP", "PULL_DOWN"]


class PinInputState(BaseModel):
    value: int
