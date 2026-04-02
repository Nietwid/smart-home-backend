from device.models import ChipType, Device
from dispatcher.device.messages.enum import MessageCommand
from hardware.base import BaseHardware, HardwareValidationError
from hardware.buzzer.extra_settings import PlaySequenceExtraSettings
from hardware.buzzer.schema import BuzzerConfig, BuzzerState
from hardware.helpers.is_used import is_used
from hardware.registry import hardware_registry
from hardware.enums import HardwareTypes


@hardware_registry(name="active_buzzer")
class ActiveBuzzerHardware(BaseHardware):
    config_model = BuzzerConfig
    state_model = BuzzerState
    hardware_type = HardwareTypes.OUTPUT
    chip_support = [name.value for name in ChipType]
    actions = {MessageCommand.PLAY_SEQUENCE: PlaySequenceExtraSettings}
    events = ()

    @classmethod
    def validate_config(cls, config: BuzzerConfig, device: Device) -> None:
        if is_used(device.peripherals.all(), "pin", [config.pin]):
            raise HardwareValidationError(
                {"pin": {"__errors": ["This pin is already used"]}}
            )

    @classmethod
    def validate_state(cls, state: BuzzerState, device: Device) -> None:
        pass
