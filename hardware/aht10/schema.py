from pydantic import BaseModel, Field
from hardware.base import BasePeripheralConfig


class Aht10Config(BasePeripheralConfig):
    address: int = Field(default=0x38, ge=0x00, le=0x7F)
    read_interval: int = Field(default=60, ge=1, title="Interval in minutes")


class Aht10State(BaseModel):
    temperature: float = Field(default=0.0, description="Temperature in Celsius")
    humidity: float = Field(default=0.0, description="Relative humidity in %")
    last_read: str = Field(default="", description="Last read time")
