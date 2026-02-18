from hardware.base import BaseHardware

HARDWARE_REGISTRY: dict[str, BaseHardware] = {}


def hardware_registry(name: str):
    def wrapper(cls):
        HARDWARE_REGISTRY[name] = cls
        return cls
    return wrapper
