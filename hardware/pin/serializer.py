from rest_framework import serializers

from device.models import Device
from hardware.helpers.is_used import is_used


class BasicPinSerializer(serializers.Serializer):
    pin = serializers.IntegerField()

    def validate_pin(self, value: int) -> int:
        device: Device = self.context.get("device")
        if not device:
            raise serializers.ValidationError("No device specified")
        if is_used(device.peripherals.all(), "pin", [value]):
            raise serializers.ValidationError("Pin already used")
        return value


class PinOutputConfigSerializer(BasicPinSerializer): ...


class PinOutputStateSerializer(BasicPinSerializer): ...


class PinInputConfigSerializer(BasicPinSerializer): ...


class PinInputStateSerializer(BasicPinSerializer): ...
