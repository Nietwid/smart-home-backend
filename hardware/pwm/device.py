from device.models import ChipType
from hardware.pwm.action_handlers.set_value import SetValue
from hardware.registry import hardware_registry
from hardware.types import HardwareTypes
from hardware.pwm.schema import PwmState, PwmConfig
from hardware.pwm.serializer import PwmStateSerializer, PwmConfigSerializer


@hardware_registry(name="pin_pwm")
class PinPwm:
    config_model = PwmConfig
    state_model = PwmState
    config_serializer = PwmConfigSerializer
    state_serializer = PwmStateSerializer
    actions = {"set_value": SetValue}
    events = {}
    hardware_type = HardwareTypes.OUTPUT
    description = "Single-channel PWM controller"
    chip_support = [name.value for name in ChipType]
