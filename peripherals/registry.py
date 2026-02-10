from pydantic import BaseModel

from peripherals.schemas.base import PeripheralDefinition
from typing import Protocol, runtime_checkable, TypeVar, Type, Any

PERIPHERAL_REGISTRY: dict[str, PeripheralDefinition] = {}


@runtime_checkable
class PeripheralSchema(Protocol):
    class Config(BaseModel): ...

    class StateSchema(BaseModel): ...


T = TypeVar("T", bound=Type[PeripheralSchema])


def register_peripheral(
    type_key: str,
    description: str,
    handler: Any = None,
    supported_events: list[str] = None,
):
    """Decorator to register a peripheral"""

    def wrapper(cls: T) -> T:
        if not isinstance(cls, PeripheralSchema):
            raise TypeError(f"{type_key} is not a PeripheralSchema")

        PERIPHERAL_REGISTRY[type_key] = PeripheralDefinition(
            description=description,
            config_schema=cls.Config,
            state_schema=cls.StateSchema,
            handler=handler if handler else None,
            supported_events=supported_events if supported_events else [],
        )
        return cls

    return wrapper
