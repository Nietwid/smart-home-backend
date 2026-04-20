from typing import Any
from hardware.helpers.extract_field import extract_field
from peripherals.models import Peripherals


def is_used(peripherals: list[Peripherals], key: str, value: list[Any]) -> bool:
    """
    Checks if any of the given values appear in the configuration fields
    of a list of peripheral devices.

    Args:
        peripherals : list[Peripherals]
            A list of Peripherals objects whose configurations will be checked.
        key : str
            The name of the field in the configuration to inspect.
        value : list[Any]
            A list of values to look for. The function returns True if at least
            one of these values is present in the specified field of any peripheral.

    Returns:
       bool : True if at least one value from `value` exists in the `key` field
        of any peripheral; False otherwise.

    """
    for peripheral in peripherals:
        fields = extract_field(peripheral.config, key)
        if any(v in fields for v in value):
            return True
    return False
