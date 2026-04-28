from typing import Literal
from pydantic import BaseModel, Field


class NumericConditionSchema(BaseModel):
    type: Literal["numeric"] = "numeric"
    operator: Literal[">", "<", ">=", "<="]
    value: float
    hysteresis: float
