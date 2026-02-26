from pydantic import BaseModel, Field
from datetime import datetime

from utils.round_timestamp_to_nearest_hour import round_timestamp_to_nearest_hour


class TimestampedRequest(BaseModel):
    timestamp: datetime = Field(default_factory=round_timestamp_to_nearest_hour)


class TemperatureRequest(TimestampedRequest):
    temperature: float


class HumidityRequest(TimestampedRequest):
    humidity: float


class TempHumRequest(TemperatureRequest, HumidityRequest):
    pass
