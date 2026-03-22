from dispatcher.device.messages.enum import MessageCommand
from device.models import ChipType, Device
from hardware.base import BaseHardware, HardwareValidationError
from hardware.registry import hardware_registry
from hardware.enums import HardwareTypes
from hardware.rtc.schema import RtcConfig, RtcState


@hardware_registry(name="rtc")
class Rtc(BaseHardware):
    config_model = RtcConfig
    state_model = RtcState
    hardware_type = HardwareTypes.OUTPUT
    chip_support = [name.value for name in ChipType]
    actions = {}
    events = (MessageCommand.ON_SYNC_TIME,)

    @classmethod
    def validate_config(cls, config: RtcConfig, device: Device) -> None:
        if device.peripherals.filter(name="rtc").exists():
            raise HardwareValidationError(
                {"__errors": ["This device already has an RTC peripheral"]}
            )

    @classmethod
    def validate_state(cls, state: RtcState, device: Device) -> None:
        pass
