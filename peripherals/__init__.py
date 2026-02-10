from pydantic import BaseModel
from typing import Type


class ComponentDefinition(BaseModel):
    display_name: str
    description: str
    config_schema: Type[BaseModel]
    state_schema: Type[BaseModel]
