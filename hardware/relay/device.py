from dispatcher.device.messages.enum import MessageCommand
from device.models import ChipType, Device
from hardware.base import BaseHardware, HardwareValidationError
from hardware.helpers.is_used import is_used
from hardware.registry import hardware_registry
from hardware.enums import HardwareTypes
from hardware.relay.extra_settings import RelayExtraSettings
from hardware.relay.schema import RelayConfig, RelayState


@hardware_registry(name="relay")
class RelayHardware(BaseHardware):
    config_model = RelayConfig
    state_model = RelayState
    hardware_type = HardwareTypes.OUTPUT
    chip_support = [name.value for name in ChipType]
    actions = {
        MessageCommand.TOGGLE: None,
        MessageCommand.ON: RelayExtraSettings,
        MessageCommand.OFF: RelayExtraSettings,
    }
    events = (
        MessageCommand.ON_ON,
        MessageCommand.ON_OFF,
    )

    @classmethod
    def validate_config(cls, config: RelayConfig, device: Device) -> None:
        if is_used(device.peripherals.all(), "pin", [config.pin]):
            raise HardwareValidationError(
                {"pin": {"__errors": ["This pin is already used"]}}
            )

    @classmethod
    def validate_state(cls, state: RelayState, device: Device) -> None:
        pass
