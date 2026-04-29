from typing import Literal
from pydantic import BaseModel


class BooleanConditionSchema(BaseModel):
    type: Literal["boolean"] = "boolean"
    value: bool
