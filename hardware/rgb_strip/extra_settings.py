from pydantic import Field, ConfigDict, field_validator, ValidationInfo
from typing import Optional

from hardware.base import BaseExtraSettings
from hardware.rgb_strip.schema import RGBStripConfig


class UpdateStateExtraSettings(BaseExtraSettings):
    model_config = ConfigDict(
        title="RGB Strip extra settings",
    )
    brightness: Optional[int] = Field(default=None, gt=0, le=100)
    is_on: Optional[bool] = None
    r_duty_cycle: Optional[int] = Field(None, ge=0)
    g_duty_cycle: Optional[int] = Field(None, ge=0)
    b_duty_cycle: Optional[int] = Field(None, ge=0)

    @field_validator("r_duty_cycle", "g_duty_cycle", "b_duty_cycle")
    def check_duty_cycle(cls, value: Optional[int], info: ValidationInfo):
        if value is None:
            return value

        config_data = info.context.get("config")
        if not config_data:
            return value

        resolution_bits = config_data.get("resolution_bits")
        max_resolution = 2**resolution_bits

        if value > max_resolution:
            raise ValueError(f"Value must be less than or equal to {max_resolution}")
        return value
