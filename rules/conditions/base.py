from typing import Union

from rules.conditions.boolean import BooleanConditionSchema
from rules.conditions.numeric import NumericConditionSchema

ConditionConfig = Union[NumericConditionSchema, BooleanConditionSchema]
