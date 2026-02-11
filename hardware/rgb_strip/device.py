from device.models import ChipType
from hardware.rgb_strip.action_handlers.set_color import SetColor
from hardware.rgb_strip.action_handlers.turn_off import TurnOff
from hardware.rgb_strip.action_handlers.turn_on import TurnOn
from hardware.rgb_strip.schema import (
    RGBStripState,
    RGBStripConfig,
)
from hardware.rgb_strip.serializer import (
    RGBStripConfigSerializer,
    RGBStripStateSerializer,
)

from hardware.registry import hardware_registry
from hardware.types import HardwareTypes


@hardware_registry(
    name="rgb_strip",
)
class RGBStrip:
    hardware_type = HardwareTypes.LIGHT
    config_model = RGBStripConfig
    state_model = RGBStripState
    config_serializer = RGBStripConfigSerializer
    state_serializer = RGBStripStateSerializer
    actions = {"set_color": SetColor, "turn_on": TurnOn, "turn_off": TurnOff}
    events = {}
    description = "RGB LED strip controller with three independent PWM outputs (R, G, B channels)."
    chip_support = [name.value for name in ChipType]
