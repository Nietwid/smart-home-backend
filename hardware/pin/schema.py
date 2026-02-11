from pydantic import BaseModel
from typing import Literal


class PinOutputConfig(BaseModel):
    pin: int


class PinOutputState(BaseModel):
    value: int


class PinInputConfig(BaseModel):
    pin: int
    mode: Literal["PULL_UP", "PULL_DOWN"]


class PinInputState(BaseModel):
    value: int
