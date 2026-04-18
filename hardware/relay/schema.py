from pydantic import Field

from hardware.pin.schema import PinOutputConfig, PinOutputState


class RelayConfig(PinOutputConfig):
    inverted: bool = Field(default=False)


class RelayState(PinOutputState): ...
