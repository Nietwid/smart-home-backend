from pydantic import BaseModel, Field

from hardware.base import BasePeripheralConfig


class RGBStripConfig(BasePeripheralConfig):
    r_pin: int = Field(..., ge=0, le=40, title="R - Channel pin")
    g_pin: int = Field(..., ge=0, le=40, title="G - Channel pin")
    b_pin: int = Field(..., ge=0, le=40, title="B - Channel pin")
    frequency: int = Field(250, title="Frequency (Hz)")
    resolution_bits: int = 8

    class Config:
        title = "RGB strip configuration"


class RGBStripState(BaseModel):
    brightness: int = Field(default=100, gt=0, le=100)
    is_on: bool = Field(default=False)
    r_duty_cycle: int = Field(default=0)
    g_duty_cycle: int = Field(default=0)
    b_duty_cycle: int = Field(default=0)
