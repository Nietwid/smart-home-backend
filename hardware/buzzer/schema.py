from pydantic import BaseModel

from hardware.pin.schema import PinOutputConfig


class BuzzerConfig(PinOutputConfig): ...


class BuzzerState(BaseModel): ...
