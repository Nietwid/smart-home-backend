from pydantic import BaseModel, Field

from hardware.base import BasePeripheralConfig
from hardware.pin.schema import PinOutputConfig


class PwmConfig(BasePeripheralConfig):
    pin: int = Field(ge=0, le=40)
    frequency: int = 250
    resolution_bits: int = 8


class PwmState(BaseModel):
    duty_cycle: int = 0
