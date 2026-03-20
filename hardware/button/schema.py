from hardware.base import BasePeripheralConfig
from pydantic import BaseModel, Field


class ButtonMonostableConfig(BasePeripheralConfig):
    pin: int = Field(ge=0, le=40)


class ButtonMonostableState(BaseModel):
    is_on: bool = Field(default=False)


class ButtonBistableConfig(BasePeripheralConfig):
    pin: int = Field(ge=0, le=40)


class ButtonBistableState(BaseModel):
    is_on: bool = Field(default=False)
