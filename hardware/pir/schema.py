from pydantic import Field

from hardware.pin.schema import PinOutputConfig, PinOutputState


class PirConfig(PinOutputConfig):
    cool_down_time: int = Field(default=5, title="Cool down time (s)")


class PirState(PinOutputState): ...
