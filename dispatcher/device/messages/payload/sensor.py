from pydantic import BaseModel

from dispatcher.device.messages.enum import ActionResult


class AddTagResult(BaseModel):
    uid: str
    status:ActionResult

class AddTagIntent(BaseModel):
    name:str

class OnReadIntent(BaseModel):
    uid: str

class OnMotionIntent(BaseModel):
    is_on: bool

class OnReadSuccessPayload(BaseModel):
    pass


class OnReadFailurePayload(BaseModel):
    pass


class AccessGrantedPayload(BaseModel):
    pass


class AccessDeniedPayload(BaseModel):
    pass
