from typing import Literal, Any

from pydantic import BaseModel


class BaseCondition(BaseModel):
    operator: Literal["==", ">", "<", ">=", "<="] = "=="
    value: Any

    @property
    def value_to_db(self):
        raise NotImplementedError
