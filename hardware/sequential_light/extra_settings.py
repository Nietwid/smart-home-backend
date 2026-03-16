from typing import Optional

from pydantic import BaseModel, Field


class BaseExtraSettings(BaseModel):
    reverse: Optional[bool] = Field(default=False)


class BlinkExtraSettings(BaseExtraSettings):
    lighting_time: int = Field(default=0)
