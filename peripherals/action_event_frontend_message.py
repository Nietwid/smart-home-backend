from typing import Optional, Dict, Any
from pydantic import BaseModel, model_validator, Field

from dispatcher.device.messages.enum import Scope, MessageType

from dispatcher.device.messages.enum import MessageCommand


class ActionEventFrontendMessage(BaseModel):
    scope: Scope
    type: MessageType
    peripheral_id: Optional[int] = Field(default=None)
    device_id: Optional[str] = Field(default=None)
    command: MessageCommand
    payload: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @model_validator(mode="after")
    def check_scope_ids(self, data):
        if self.scope == Scope.PERIPHERAL and not self.peripheral_id:
            raise ValueError("peripheral_id is required when scope is 'peripheral'")
        if self.scope == Scope.CPU and not self.device_id:
            raise ValueError("device_id is required when scope is 'cpu'")
        return data
