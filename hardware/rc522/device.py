from dispatcher.device.messages.enum import MessageCommand
from device.models import ChipType, Device
from hardware.base import BaseHardware, HardwareValidationError
from hardware.helpers.is_used import is_used
from hardware.rc522.schema import Rc552Config, Rc552State
from hardware.registry import hardware_registry
from hardware.enums import HardwareTypes


@hardware_registry(name="rc522")
class Rc522(BaseHardware):
    config_model = Rc552Config
    state_model = Rc552State
    hardware_type = HardwareTypes.SENSOR
    chip_support = [name.value for name in ChipType]
    actions = {
        MessageCommand.ADD_TAG: None,
    }
    events = (
        MessageCommand.ON_READ,
        MessageCommand.ON_READ_SUCCESS,
        MessageCommand.ON_READ_FAILURE,
    )

    @classmethod
    def validate_config(cls, config: Rc552Config, device: Device) -> None:
        if is_used(device.peripherals.all(), "pin", [config.ss, config.rst]):
            raise HardwareValidationError(
                {"pin": {"__errors": ["This pin is already used"]}}
            )

    @classmethod
    def validate_state(cls, state: Rc552State, device: Device) -> None:
        pass
