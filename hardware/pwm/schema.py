from pydantic import BaseModel, Field

from hardware.base import BasePeripheralConfig
from hardware.pin.schema import PinOutputConfig


class PwmConfig(BasePeripheralConfig):
    pin: PinOutputConfig
    frequency: int = 250
    resolution_bits: int = 8


class PwmState(BaseModel):
    duty_cycle: int = 0
