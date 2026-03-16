from pydantic import BaseModel, Field
from typing import Optional


class UpdateStateExtraSettings(BaseModel):
    brightness: Optional[int] = Field(gt=0, le=100)
    is_on: Optional[bool] = Field(default=False)
