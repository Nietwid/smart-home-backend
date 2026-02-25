from consumers.device.messages.enum import MessageEvent
from device.models import ChipType, Device
from hardware.base import BaseHardware, HardwareValidationError
from hardware.helpers.is_used import is_used
from hardware.registry import hardware_registry
from hardware.enums import HardwareTypes
from hardware.pin.schema import (
    PinOutputConfig,
    PinInputState,
    PinOutputState,
    PinInputConfig,
)


@hardware_registry(name="pin_output")
class PinInputHardware(BaseHardware):
    description = "Digital output pin."
    config_model = PinOutputConfig
    state_model = PinOutputState
    hardware_type = HardwareTypes.OUTPUT
    chip_support = [name.value for name in ChipType]
    actions = (MessageEvent.SET_VALUE,)
    events = ()

    @classmethod
    def validate_config(cls, config: PinOutputConfig, device: Device) -> None:
        if is_used(device.peripherals.all(), "pin", [config.pin]):
            raise HardwareValidationError(
                {"pin": {"__errors": ["This pin is already used"]}}
            )

    @classmethod
    def validate_state(cls, state: PinOutputState, device: Device) -> None:
        pass


@hardware_registry(name="pin_input")
class PinOutputHardware(BaseHardware):
    config_model = PinInputConfig
    state_model = PinInputState
    hardware_type = HardwareTypes.INPUT
    description = "Digital input pin."
    chip_support = [name.value for name in ChipType]
    actions = (MessageEvent.SET_VALUE,)
    events = ()

    @classmethod
    def validate_config(cls, config: PinInputConfig, device: Device) -> None:
        if is_used(device.peripherals.all(), "pin", [config.pin]):
            raise HardwareValidationError(
                {"pin": {"__errors": ["This pin is already used"]}}
            )

    @classmethod
    def validate_state(cls, state: PinInputState, device: Device) -> None:
        pass
