from rest_framework import serializers

from hardware.registry import HARDWARE_REGISTRY
from peripherals.models import Peripherals
from rules.models import RuleTrigger


class RuleTriggerFrontendSerializer(serializers.ModelSerializer):
    peripheral_name = serializers.SerializerMethodField()
    device_name = serializers.SerializerMethodField()

    class Meta:
        model = RuleTrigger
        fields = ["id", "event", "extra_settings", "peripheral_name", "device_name"]

    def get_peripheral_name(self, obj: RuleTrigger):
        return obj.peripheral.name

    def get_device_name(self, obj: RuleTrigger):
        return obj.peripheral.device.name


class RuleTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleTrigger
        fields = "__all__"

    def validate(self, data: dict) -> dict:
        peripheral: Peripherals = data.get("peripheral")
        event = data.get("event")
        registry = HARDWARE_REGISTRY.get(peripheral.name)

        if registry is None:
            raise serializers.ValidationError(
                f"The selected peripheral ({peripheral.name}) is not supported."
            )

        if not event in registry.get_available_events():
            raise serializers.ValidationError(
                f"The selected event ({event}) is not supported for the selected peripheral."
            )
        return data
