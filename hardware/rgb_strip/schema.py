from pydantic import BaseModel

from hardware.pwm.schema import PwmConfig, PwmState


class RGBStripConfig(BaseModel):
    r_pin: PwmConfig
    g_pin: PwmConfig
    b_pin: PwmConfig


class RGBStripState(BaseModel):
    r_pin: PwmState
    g_pin: PwmState
    b_pin: PwmState
