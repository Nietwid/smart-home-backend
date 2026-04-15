from pydantic import BaseModel, Field, field_validator, model_validator
from hardware.pca9685.schema import Pca9685Config
from typing import Union


class LightingPeriod(BaseModel):
    start_time: int
    end_time: int
    brightness: int = Field(..., gt=0, le=100)

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_time_string(cls, v: Union[str, int]) -> int:
        if isinstance(v, int):
            return v

        if isinstance(v, str) and ":" in v:
            try:
                # Split "hh:mm:ss"
                parts = [int(p) for p in v.split(":")]
                if len(parts) == 3:  # hh:mm:ss
                    return parts[0] * 3600 + parts[1] * 60 + parts[2]
                if len(parts) == 2:  # hh:mm
                    return parts[0] * 3600 + parts[1] * 60
            except ValueError:
                raise ValueError("Time string must be in the format hh:mm:ss or hh:mm")
        return v


class SequentialLightConfig(Pca9685Config):
    address: int = Field(default=0x40, ge=0x00, le=0x7F)
    frequency: int = Field(default=500, ge=50, le=1500)
    light_count: int = Field(default=16, gt=0, le=16)


class SequentialLightState(BaseModel):
    is_on: bool = Field(default=False)
    brightness: int = Field(default=100, ge=0, le=100)
    speed: int = Field(default=100, ge=0, le=100)
    lighting_time: int = Field(default=10, gt=0)
    lighting_period: list[LightingPeriod] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate(self, data):
        print(data)
        return data
