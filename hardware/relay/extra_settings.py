from pydantic import Field
from typing import Optional
from hardware.base import BaseExtraSettings


class RelayExtraSettings(BaseExtraSettings):
    duration: Optional[int] = Field(None)
    delay: Optional[int] = Field(None)
