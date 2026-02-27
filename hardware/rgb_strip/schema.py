from pydantic import BaseModel, Field

from hardware.pwm.schema import PwmConfig, PwmState


class RGBStripConfig(BaseModel):
    r_pin: PwmConfig
    g_pin: PwmConfig
    b_pin: PwmConfig


class RGBStripState(BaseModel):
    brightness: int = Field(default=100, gt=0, le=100)
    r_pin: PwmState = PwmState()
    g_pin: PwmState = PwmState()
    b_pin: PwmState = PwmState()
