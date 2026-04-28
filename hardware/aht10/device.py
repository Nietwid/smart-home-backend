from dispatcher.device.messages.enum import MessageCommand
from device.models import ChipType, Device
from hardware.aht10.schema import Aht10Config, Aht10State
from hardware.base import BaseHardware, HardwareValidationError
from hardware.helpers.is_used import is_used
from hardware.registry import hardware_registry
from hardware.enums import HardwareTypes
from rules.conditions.numeric import NumericConditionSchema


@hardware_registry(name="aht10")
class Aht10(BaseHardware):
    config_model = Aht10Config
    state_model = Aht10State
    hardware_type = HardwareTypes.SENSOR
    chip_support = [name.value for name in ChipType]
    actions = {}
    events = {
        MessageCommand.ON_MEASURE_TEMPERATURE: NumericConditionSchema,
        MessageCommand.ON_MEASURE_HUMIDITY: NumericConditionSchema,
    }
    event_to_attr = {
        MessageCommand.ON_MEASURE_TEMPERATURE: "temperature",
        MessageCommand.ON_MEASURE_HUMIDITY: "humidity",
    }

    @classmethod
    def validate_config(cls, config: Aht10Config, device: Device) -> None:
        if is_used(device.peripherals.all(), "address", [config.address]):
            raise HardwareValidationError(
                {"address": {"__errors": ["This address is already used"]}}
            )
        if not device.peripherals.filter(name="rtc").exists():
            raise HardwareValidationError(
                {"__errors": ["This device must have an RTC activated"]}
            )

    @classmethod
    def validate_state(cls, state: Aht10State, device: Device) -> None:
        pass
