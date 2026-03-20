from pydantic import BaseModel, Field

from hardware.base import BasePeripheralConfig


class Rc552Config(BasePeripheralConfig):
    ss: int = Field(ge=0, le=40)
    cs: int = Field(ge=0, le=40)


class Rc552State(BaseModel): ...
