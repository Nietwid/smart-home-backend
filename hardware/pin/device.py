from device.models import ChipType
from hardware.pin.action_handlers.output_set_value import OutputSetValue
from hardware.pin.action_handlers.set_value import SetValue
from hardware.registry import hardware_registry
from hardware.types import HardwareTypes
from hardware.pin.schema import (
    PinOutputConfig,
    PinInputState,
    PinOutputState,
    PinInputConfig,
)
from hardware.pin.serializer import (
    PinInputStateSerializer,
    PinInputConfigSerializer,
    PinOutputConfigSerializer,
    PinOutputStateSerializer,
)


@hardware_registry(name="pin_output")
class PinOutput:
    config_model = PinOutputConfig
    state_model = PinOutputState
    config_serializer = PinOutputConfigSerializer
    state_serializer = PinOutputStateSerializer
    actions = {"set_value": OutputSetValue}
    events = {}
    hardware_type = HardwareTypes.OUTPUT
    description = "Digital output pin."
    chip_support = [name.value for name in ChipType]


@hardware_registry(name="pin_input")
class PinOutput:
    config_model = PinInputConfig
    state_model = PinInputState
    config_serializer = PinInputConfigSerializer
    state_serializer = PinInputStateSerializer
    actions = {"set_value": SetValue}
    events = {}
    hardware_type = HardwareTypes.INPUT
    description = "Digital input pin."
    chip_support = [name.value for name in ChipType]
