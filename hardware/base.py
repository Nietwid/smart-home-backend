from abc import ABC, abstractmethod
from typing import Type, Optional
from pydantic import BaseModel, Field

from device.models import Device
from dispatcher.device.messages.enum import MessageCommand
from typing import Collection


class BaseHardware(ABC):
    config_model: Type[BaseModel] = None
    state_model: Type[BaseModel] = None

    description: str = ""
    hardware_type: str = ""
    chip_support: tuple[str] = []
    actions: dict[MessageCommand, Type[BaseModel]] = {}
    events: tuple[str] = []

    @classmethod
    def parse_config(cls, data: dict) -> BaseModel:
        if cls.config_model is None:
            raise NotImplementedError()
        return cls.config_model(**data)

    @classmethod
    def parse_state(cls, data: dict) -> BaseModel:
        if cls.config_model is None:
            raise NotImplementedError()
        return cls.state_model(**data)

    @classmethod
    def get_available_actions(cls) -> Collection[MessageCommand]:
        return cls.actions.keys()

    @classmethod
    @abstractmethod
    def validate_config(cls, config: Type[BaseModel], device: Device) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def validate_state(cls, state: Type[BaseModel], device: Device) -> None:
        raise NotImplementedError()


class HardwareValidationError(Exception):
    def __init__(self, errors: dict):
        self.errors = errors
        super().__init__(str(errors))


class BasePeripheralConfig(BaseModel):
    name: str = Field(default=None)
