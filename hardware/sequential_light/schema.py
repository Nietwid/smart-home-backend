from pydantic import BaseModel, Field
from hardware.pca9685.schema import Pca9685Config


class SequentialLightConfig(Pca9685Config):
    address: int = Field(default=0x40, ge=0x00, le=0x7F)
    frequency: int = Field(default=50, ge=50, le=1500)
    light_count: int = Field(default=16)


class SequentialLightState(BaseModel):
    brightness: int = Field(default=100)
    step: int = Field(default=100)
    lighting_time: int = Field(default=10)
