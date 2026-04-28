from pydantic import ValidationError
from rest_framework import serializers

from dispatcher.device.messages.enum import MessageEvent
from hardware.registry import HARDWARE_REGISTRY
from peripherals.models import Peripherals
from rules.models import RuleCondition


class RuleConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleCondition
        fields = "__all__"

    def validate(self, data: dict) -> dict:
        peripheral: Peripherals = data.get("peripheral")
        if peripheral is None:
            raise serializers.ValidationError("Peripheral is required")

        condition: dict | None = data.get("condition")
        if condition is None:
            raise serializers.ValidationError("Condition is required")

        hardware_cls = HARDWARE_REGISTRY.get(peripheral.name)
        if hardware_cls is None:
            raise serializers.ValidationError("Peripheral is not supported")

        event: str | None = data.get("event")
        if event is None:
            raise serializers.ValidationError("Event is required")

        condition_cls = hardware_cls.events.get(event)
        if condition_cls is None:
            raise serializers.ValidationError("Event is not supported")

        try:
            condition_cls(**condition)
            return data
        except ValidationError as e:
            errors = {"condition": {}}
            for err in e.errors():
                path = ".".join(str(x) for x in err["loc"])
                errors["condition"][f"{path}"] = err["msg"]
            raise serializers.ValidationError(errors)
