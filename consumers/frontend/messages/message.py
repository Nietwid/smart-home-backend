from pydantic import BaseModel

from consumers.frontend.messages.types import (
    FrontendMessageType,
)


class FrontendMessage(BaseModel):
    action: FrontendMessageType
    status: int
    data: dict
