from dispatcher.device.messages.enum import MessageCommand
from device.models import ChipType, Device
from hardware.base import BaseHardware, HardwareValidationError
from hardware.helpers.is_used import is_used
from hardware.registry import hardware_registry
from hardware.enums import HardwareTypes
from hardware.button.schema import (
    ButtonBistableState,
    ButtonBistableConfig,
    ButtonMonostableState,
    ButtonMonostableConfig,
)


@hardware_registry(name="button_bistable")
class ButtonBistableHardware(BaseHardware):
    config_model = ButtonMonostableConfig
    state_model = ButtonMonostableState
    hardware_type = HardwareTypes.OUTPUT
    chip_support = [name.value for name in ChipType]
    actions = {MessageCommand.TOGGLE: None}
    events = (
        MessageCommand.ON_ON,
        MessageCommand.ON_OFF,
    )

    @classmethod
    def validate_config(cls, config: ButtonBistableConfig, device: Device) -> None:
        if is_used(device.peripherals.all(), "pin", [config.pin]):
            raise HardwareValidationError(
                {"pin": {"__errors": ["This pin is already used"]}}
            )

    @classmethod
    def validate_state(cls, state: ButtonBistableState, device: Device) -> None:
        pass


@hardware_registry(name="button_monostable")
class ButtonMonostableHardware(BaseHardware):
    config_model = ButtonBistableConfig
    state_model = ButtonBistableState
    hardware_type = HardwareTypes.INPUT
    chip_support = [name.value for name in ChipType]
    actions = {MessageCommand.CLICK: None, MessageCommand.HOLD: None}
    events = (
        MessageCommand.ON_CLICK,
        MessageCommand.ON_HOLD,
    )

    @classmethod
    def validate_config(cls, config: ButtonBistableConfig, device: Device) -> None:
        if is_used(device.peripherals.all(), "pin", [config.pin]):
            raise HardwareValidationError(
                {"pin": {"__errors": ["This pin is already used"]}}
            )

    @classmethod
    def validate_state(cls, state: ButtonBistableState, device: Device) -> None:
        pass
