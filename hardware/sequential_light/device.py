from dispatcher.device.messages.enum import MessageCommand
from device.models import ChipType, Device
from hardware.base import BaseHardware, HardwareValidationError
from hardware.helpers.is_used import is_used
from hardware.registry import hardware_registry
from hardware.enums import HardwareTypes
from hardware.sequential_light.extra_settings import (
    BlinkExtraSettings,
    LightBaseExtraSettings,
)
from hardware.sequential_light.schema import (
    SequentialLightState,
    SequentialLightConfig,
)


@hardware_registry(name="sequential_light")
class SequentialLightHardware(BaseHardware):
    config_model = SequentialLightConfig
    state_model = SequentialLightState
    hardware_type = HardwareTypes.OUTPUT
    chip_support = [name.value for name in ChipType]
    actions = {
        MessageCommand.ON: LightBaseExtraSettings,
        MessageCommand.OFF: LightBaseExtraSettings,
        MessageCommand.TOGGLE: LightBaseExtraSettings,
        MessageCommand.BLINK: BlinkExtraSettings,
        MessageCommand.UPDATE_STATE: None,
    }
    events = (
        MessageCommand.ON_ON,
        MessageCommand.ON_OFF,
        MessageCommand.ON_BLINK,
        MessageCommand.ON_UPDATE_STATE,
    )

    @classmethod
    def validate_config(cls, config: SequentialLightConfig, device: Device) -> None:
        if is_used(device.peripherals.all(), "address", [config.address]):
            raise HardwareValidationError(
                {"address": {"__errors": ["This address is already used"]}}
            )

    @classmethod
    def validate_state(cls, state: SequentialLightState, device: Device) -> None:
        pass
