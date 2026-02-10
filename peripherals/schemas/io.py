from pydantic import BaseModel


class PWMConfig(BaseModel):
    pin: int
    frequency: int = 1000
    resolution_bits: int = 8


class PWMState(BaseModel):
    duty_cycle: int = 0
