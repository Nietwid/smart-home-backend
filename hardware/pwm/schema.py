from pydantic import BaseModel

from hardware.base import BaseHardwareSchema


class PwmConfig(BaseHardwareSchema):
    pin: int
    frequency: int = 250
    resolution_bits: int = 8


class PwmState(BaseModel):
    duty_cycle: int = 0
