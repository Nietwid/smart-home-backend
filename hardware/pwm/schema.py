from pydantic import BaseModel


class PwmConfig(BaseModel):
    pin: int
    frequency: int = 250
    resolution_bits: int = 8


class PwmState(BaseModel):
    duty_cycle: int = 0
