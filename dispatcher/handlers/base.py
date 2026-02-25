from abc import ABC, abstractmethod

from dispatcher.command_message.message import CommandMessage


class ActionEventBaseHandler(ABC):
    @abstractmethod
    def __call__(self, message: CommandMessage):
        raise NotImplementedError()
