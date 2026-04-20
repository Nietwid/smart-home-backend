from pydantic import BaseModel, Field

from hardware.base import BasePeripheralConfig


class RtcConfig(BasePeripheralConfig): ...


class RtcState(BaseModel): ...
