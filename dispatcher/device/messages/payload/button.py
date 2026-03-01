from pydantic import BaseModel

from dispatcher.device.messages.payload.basic import BasicResult


class ToggleResult(BasicResult):
    is_on: bool


class OnClickPayload(BaseModel):
    pass


class OnHoldPayload(BaseModel):
    pass
