from abc import ABC, abstractmethod

from dispatcher.command_message.message import CommandMessage
from dispatcher.dispatch_result import DispatchResult


class ActionEventBaseHandler(ABC):
    @abstractmethod
    def __call__(self, message: CommandMessage) -> DispatchResult:
        raise NotImplementedError()
