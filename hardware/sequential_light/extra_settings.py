from typing import Optional

from pydantic import Field

from hardware.base import BaseExtraSettings


class LightBaseExtraSettings(BaseExtraSettings):
    reverse: Optional[bool] = Field(default=False)


class BlinkExtraSettings(LightBaseExtraSettings):
    lighting_time: Optional[int] = Field(default=0)
