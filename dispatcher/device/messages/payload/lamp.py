from pydantic import BaseModel
import enum
class OnBlinkStatus(enum.Enum):
    START = 1
    STOP = 2

class OnPayload(BaseModel):
    pass


class OffPayload(BaseModel):
    pass


class BlinkPayload(BaseModel):
    pass

class OnBlinkPayload(BaseModel):
    status: OnBlinkStatus