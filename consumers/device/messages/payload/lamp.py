from pydantic import BaseModel

class OnPayload(BaseModel):
    pass


class OffPayload(BaseModel):
    pass


class BlinkPayload(BaseModel):
    pass

class TogglePayload(BaseModel):
    pass
