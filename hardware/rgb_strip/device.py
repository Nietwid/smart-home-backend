from dispatcher.device.messages.enum import MessageCommand
from device.models import ChipType, Device
from hardware.base import BaseHardware, HardwareValidationError
from hardware.helpers.extract_field import extract_field
from hardware.rgb_strip.extra_settings import UpdateStateExtraSettings
from hardware.rgb_strip.schema import (
    RGBStripState,
    RGBStripConfig,
)
from hardware.registry import hardware_registry
from hardware.enums import HardwareTypes


@hardware_registry(name="rgb_strip")
class RGBStripHardware(BaseHardware):
    config_model = RGBStripConfig
    state_model = RGBStripState
    hardware_type = HardwareTypes.LIGHT
    chip_support = [name.value for name in ChipType]
    actions = {
        MessageCommand.UPDATE_STATE: UpdateStateExtraSettings,
        MessageCommand.TOGGLE: None,
    }
    events = ()

    @classmethod
    def validate_config(cls, config: RGBStripConfig, device: Device) -> None:
        occupied_pins = []
        for peripheral in device.peripherals.all():
            occupied_pins.extend(extract_field(peripheral.config, "pin"))

        errors = {}

        for color in ["r_pin", "g_pin", "b_pin"]:
            pin_value = getattr(config, color).pin
            if pin_value in occupied_pins:
                errors.setdefault(color, {})["__errors"] = ["This pin is already used"]

        if errors:
            raise HardwareValidationError(errors)

    @classmethod
    def validate_state(cls, state: RGBStripState, device: Device) -> None:
        pass
