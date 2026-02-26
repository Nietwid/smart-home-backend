from pydantic import BaseModel


class AddTagRequest(BaseModel):
    name: str


class AddTagResponse(BaseModel):
    name: str
    uid: int


class OnReadRequest(BaseModel):
    uid: int


class OnReadSuccessPayload(BaseModel):
    pass


class OnReadFailurePayload(BaseModel):
    pass


class AccessGrantedPayload(BaseModel):
    pass


class AccessDeniedPayload(BaseModel):
    pass
