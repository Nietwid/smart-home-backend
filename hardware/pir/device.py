from dispatcher.device.messages.enum import MessageCommand
from device.models import ChipType, Device
from hardware.base import BaseHardware, HardwareValidationError
from hardware.helpers.is_used import is_used
from hardware.pir.schema import PirConfig, PirState
from hardware.registry import hardware_registry
from hardware.enums import HardwareTypes
from rules.conditions.boolean import BooleanConditionSchema


@hardware_registry(name="pir_sensor")
class PirHardware(BaseHardware):
    config_model = PirConfig
    state_model = PirState
    hardware_type = HardwareTypes.SENSOR
    chip_support = [name.value for name in ChipType]
    actions = {}
    events = {MessageCommand.ON_MOTION: BooleanConditionSchema}
    event_to_attr = {
        MessageCommand.ON_MOTION: "is_on",
    }

    @classmethod
    def validate_config(cls, config: PirConfig, device: Device) -> None:
        if is_used(device.peripherals.all(), "pin", [config.pin]):
            raise HardwareValidationError(
                {"pin": {"__errors": ["This pin is already used"]}}
            )

    @classmethod
    def validate_state(cls, state: PirState, device: Device) -> None:
        pass
