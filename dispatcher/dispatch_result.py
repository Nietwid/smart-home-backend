from pydantic import BaseModel, Field

from dispatcher.command_message.message import CommandMessage
from notifier.message import NotifierMessage


class DispatchResult(BaseModel):
    notifications: list[NotifierMessage] = Field(default_factory=list)
    commands: list[CommandMessage] = Field(default_factory=list)
