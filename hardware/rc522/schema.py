from pydantic import BaseModel, Field

from hardware.base import BasePeripheralConfig
from hardware.pin.schema import PinOutputConfig


class Rc552Config(BasePeripheralConfig):
    ss: PinOutputConfig
    cs: PinOutputConfig


class Rc552State(BaseModel): ...
