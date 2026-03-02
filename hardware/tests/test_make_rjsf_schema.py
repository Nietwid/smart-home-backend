from hardware.pin.schema import PinOutputConfig
from hardware.registry import hardware_registry
from hardware.repository import HardwareSchemaRepository
from hardware.rgb_strip.schema import RGBStripConfig
import json


def test_make_rjsf_schema():
    print(json.dumps(HardwareSchemaRepository.get_configs(), indent=2))
