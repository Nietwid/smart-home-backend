from consumers.router_message.message_event import MessageEvent
from device.models import ChipType, Device
from hardware.base import BaseHardware, HardwareValidationError
from hardware.helpers.is_used import is_used
from hardware.pwm.action_handlers.set_value import SetValue
from hardware.registry import hardware_registry
from hardware.types import HardwareTypes
from hardware.pwm.schema import PwmState, PwmConfig


@hardware_registry(name="pin_pwm")
class PinPwm(BaseHardware):
    description = "Single-channel PWM controller"
    config_model = PwmConfig
    state_model = PwmState
    actions = {MessageEvent.SET_VALUE: SetValue}
    events = {}
    hardware_type = HardwareTypes.OUTPUT
    chip_support = [name.value for name in ChipType]

    @classmethod
    def validate_config(cls, config: PwmConfig, device: Device) -> None:
        if is_used(device.peripherals.all(), "pin", [config.pin]):
            raise HardwareValidationError(
                {"pin": {"__errors": ["This pin is already used"]}}
            )

    @classmethod
    def validate_state(cls, state: PwmState, device: Device) -> None:
        pass
