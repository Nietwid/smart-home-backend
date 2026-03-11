from rest_framework import serializers

from hardware.registry import HARDWARE_REGISTRY
from peripherals.models import Peripherals
from rules.models import RuleAction


class RuleActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleAction
        fields = "__all__"

    def validate(self, data: dict) -> dict:
        peripheral: Peripherals = data.get("peripheral")
        action = data.get("action")
        registry = HARDWARE_REGISTRY.get(peripheral.name)

        if registry is None:
            raise serializers.ValidationError(
                f"The selected peripheral ({peripheral.name}) is not supported."
            )

        if not action in registry.actions:
            raise serializers.ValidationError(
                f"The selected action ({action}) is not supported for the selected peripheral."
            )
        return data
