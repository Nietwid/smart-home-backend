from abc import ABC, abstractmethod
from typing import Type
from pydantic import BaseModel

from device.models import Device

class BaseHardware(ABC):
    config_model = None
    state_model = None

    description: str = ""
    hardware_type: str = ""
    chip_support: tuple[str] = []
    actions: tuple[str] = []
    events: tuple[str] = []

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
