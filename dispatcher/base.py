from typing import Type
from abc import ABC, abstractmethod
from pydantic import BaseModel

from dispatcher.messages.device_message import DeviceMessage
from dispatcher.messages.frontend_message import FrontendActionMessage


class DeviceBaseHandler(ABC):
    @abstractmethod
    def __call__(self, message: DeviceMessage, context: Type[BaseModel]):
        raise NotImplementedError()


class FrontendBaseHandler(ABC):
    @abstractmethod
    def __call__(self, message: FrontendActionMessage, context: Type[BaseModel]):
        raise NotImplementedError()
