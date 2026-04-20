from pydantic import BaseModel


class MeasurementIntent(BaseModel):
    value: float
