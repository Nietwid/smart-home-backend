from pydantic import ValidationError
from rest_framework import serializers

from hardware.registry import HARDWARE_REGISTRY
from peripherals.models import Peripherals
from rules.models import RuleCondition


class RuleConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleCondition
        fields = "__all__"

    def validate(self, data: dict) -> dict:
        peripheral: Peripherals = data.get("peripheral")
        if not peripheral:
            raise serializers.ValidationError("Peripheral is required")

        hardware_cls = HARDWARE_REGISTRY.get(peripheral.name)
        if not hardware_cls:
            raise serializers.ValidationError("Peripheral is not supported")

        event = data.get("event")
        if not event:
            raise serializers.ValidationError("Event is required")

        condition_cls = hardware_cls.event_conditions.get(event)
        if not condition_cls:
            raise serializers.ValidationError("Event is not supported")

        try:
            instance = condition_cls(operator=data["operator"], value=data["value"])
            data["value"] = instance.value_to_db
            return data
        except ValidationError as e:
            errors = {"condition": {}}
            for err in e.errors():
                path = ".".join(str(x) for x in err["loc"])
                errors["condition"][f"{path}"] = err["msg"]
            raise serializers.ValidationError(errors)
