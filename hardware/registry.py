from typing import Type
from pydantic import BaseModel
from rest_framework.serializers import Serializer

from hardware.base import RequestResponseInterface
from hardware.types import HardwareTypes


class RegistryInstance(BaseModel):
    config_model: Type[BaseModel]
    state_model: Type[BaseModel]
    config_serializer: Type[Serializer]
    state_serializer: Type[Serializer]
    actions: dict[str, Type[RequestResponseInterface]]
    events: dict[str, Type[RequestResponseInterface]]
    hardware_type: HardwareTypes
    description: str
    chip_support:list[str]


HARDWARE_REGISTRY: dict[str, RegistryInstance] = {}


def hardware_registry(name: str):
    def wrapper(cls):
        HARDWARE_REGISTRY[name] = RegistryInstance(
            config_model=getattr(cls, "config_model"),
            state_model=getattr(cls, "state_model"),
            config_serializer=getattr(cls, "config_serializer"),
            state_serializer=getattr(cls, "state_serializer"),
            actions=getattr(cls, "actions"),
            events=getattr(cls, "events"),
            hardware_type=getattr(cls, "hardware_type"),
            description=getattr(cls, "description"),
            chip_support=getattr(cls, "chip_support"),
        )
        return cls

    return wrapper
