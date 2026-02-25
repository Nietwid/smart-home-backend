from pydantic import BaseModel, Field

from consumers.frontend.messages.types import (
    FrontendMessageType,
)


class FrontendMessage(BaseModel):
    action: FrontendMessageType
    status: int = Field(default=200)
    data: dict
