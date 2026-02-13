from rest_framework import serializers
from device.models import Device
from hardware.helpers.is_used import is_used


class RGBStripConfigSerializer(serializers.Serializer):
    r_pin = serializers.JSONField()
    g_pin = serializers.JSONField()
    b_pin = serializers.JSONField()

    def validate(self, value):
        device: Device = self.context.get("device")
        pins = [value["r_pin"]["pin"], value["g_pin"]["pin"], value["b_pin"]["pin"]]
        if is_used(device.peripherals.all(), "pin", pins):
            raise serializers.ValidationError(
                "One of the pins is already used in this device."
            )
        return value


class RGBStripStateSerializer(serializers.Serializer): ...
