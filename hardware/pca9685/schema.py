from pydantic import BaseModel, Field

from hardware.base import BasePeripheralConfig


class Pca9685Config(BasePeripheralConfig):
    address: int = Field(default=0x40, ge=0x00, le=0x7F)
    frequency: int = Field(default=50, ge=24, le=1500)


class Pca9685State(BaseModel):
    channels: list[int] = Field(default_factory=lambda: [0] * 16)
