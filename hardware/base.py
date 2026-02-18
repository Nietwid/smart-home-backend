from abc import ABC, abstractmethod
from typing import Type
from pydantic import BaseModel

from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.message_event import MessageEvent
from device.models import Device


class EventHandler(ABC):
    @classmethod
    @abstractmethod
    def handle_event(cls, message: DeviceMessage) -> None:
        raise NotImplementedError()

class ActionHandler(ABC):

    @classmethod
    @abstractmethod
    def handle_action(cls) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def handle_response(cls, message: DeviceMessage) -> None:
        raise NotImplementedError()

class BaseHardware(ABC):
    config_model = None
    state_model = None

    description: str = ""
    hardware_type: str = ""
    chip_support: list[str] = []
    actions: dict[MessageEvent, type[ActionHandler]] = []
    events: dict[MessageEvent, type[EventHandler]] = []

    @classmethod
    def parse_config(cls, data: dict)->Type[BaseModel]:
        return cls.config_model(**data)

    @classmethod
    def parse_state(cls, data: dict)->Type[BaseModel]:
        return cls.state_model(**data)

    @classmethod
    @abstractmethod
    def validate_config(cls, config:Type[BaseModel], device:Device)->None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def validate_state(cls, state:Type[BaseModel], device:Device)->None:
        raise NotImplementedError()

class HardwareValidationError(Exception):
    def __init__(self, errors: dict):
        self.errors = errors
        super().__init__(str(errors))