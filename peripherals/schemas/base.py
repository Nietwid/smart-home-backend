from pydantic import BaseModel
from typing import Type, Any, Optional


class PeripheralDefinition(BaseModel):
    description: str
    config_schema: Type[BaseModel]
    state_schema: Type[BaseModel]
    handler: Optional[Any] = None
    supported_events: list[str]
