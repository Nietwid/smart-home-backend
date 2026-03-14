from pydantic import BaseModel
from .enum import StartSyncType

class UpdatePeripheralIntentPayload(BaseModel):
    peripheral_id: int

class UpdateRuleIntentPayload(BaseModel):
    rule_id: int


class StartSyncPayload(BaseModel):
    sync_type: StartSyncType
