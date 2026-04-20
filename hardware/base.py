from abc import ABC, abstractmethod
from typing import Type
from pydantic import BaseModel, Field, ConfigDict

from device.models import Device
from dispatcher.device.messages.enum import MessageCommand
from rules.conditions.base import BaseCondition


class BaseHardware(ABC):
    config_model: Type[BaseModel] = None
    state_model: Type[BaseModel] = None

    description: str = ""
    hardware_type: str = ""
    chip_support: tuple[str] = []
    actions: dict[MessageCommand, Type[BaseModel]] = {}
    events: tuple[str] = []
    event_conditions: dict[str, Type[BaseCondition]] = {}

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
    def get_available_actions(cls) -> list[MessageCommand]:
        return list(cls.actions.keys())

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
    name: str = Field(default="")


def clean_schema(schema):
    for prop in schema.get("properties", {}).values():
        if "anyOf" in prop:
            non_null = [x for x in prop["anyOf"] if x.get("type") != "null"]
            if non_null:
                prop.clear()
                prop.update(non_null[0])

        if prop.get("default") is None:
            prop.pop("default", None)


class BaseExtraSettings(BaseModel):
    model_config = ConfigDict(
        json_schema_extra=lambda schema, model: clean_schema(schema),
    )
