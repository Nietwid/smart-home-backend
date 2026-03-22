from pydantic import BaseModel, model_serializer
from typing import Literal
import datetime

from rules.conditions.base import BaseCondition


class TimeCondition(BaseCondition):
    value: datetime.time

    @property
    def value_to_db(self):
        return self.value.hour * 60 + self.value.minute
