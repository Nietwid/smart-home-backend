from dispatcher.device.messages.enum import MessageCommand
from device.models import ChipType, Device
from hardware.base import BaseHardware, HardwareValidationError
from hardware.helpers.is_used import is_used
from hardware.registry import hardware_registry
from hardware.enums import HardwareTypes
from hardware.pca9685.schema import (
    Pca9685Config,
    Pca9685State,
)


@hardware_registry(name="pca9685")
class PinOutputHardware(BaseHardware):
    config_model = Pca9685Config
    state_model = Pca9685State
    hardware_type = HardwareTypes.OUTPUT
    chip_support = [name.value for name in ChipType]
    actions = ()
    events = ()

    @classmethod
    def validate_config(cls, config: Pca9685Config, device: Device) -> None:
        if is_used(device.peripherals.all(), "address", [config.address]):
            raise HardwareValidationError(
                {"address": {"__errors": ["This address is already used"]}}
            )

    @classmethod
    def validate_state(cls, state: Pca9685State, device: Device) -> None:
        pass
