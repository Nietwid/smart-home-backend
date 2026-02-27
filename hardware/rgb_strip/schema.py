from pydantic import BaseModel

from hardware.base import BaseHardwareSchema
from hardware.pwm.schema import PwmConfig, PwmState


class RGBStripConfig(BaseHardwareSchema):
    r_pin: PwmConfig
    g_pin: PwmConfig
    b_pin: PwmConfig


class RGBStripState(BaseModel):
    r_pin: PwmState = PwmState()
    g_pin: PwmState = PwmState()
    b_pin: PwmState = PwmState()
