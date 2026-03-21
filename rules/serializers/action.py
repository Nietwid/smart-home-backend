from pydantic import ValidationError
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

        if not action in registry.get_available_actions():
            raise serializers.ValidationError(
                f"The selected action ({action}) is not supported for the selected peripheral."
            )

        extra_settings = data.get("extra_settings")
        if not extra_settings:
            return data

        extra_settings_model = registry.actions[action]
        if not extra_settings_model:
            return data
        try:
            extra_settings_model.model_validate(
                data["extra_settings"], context={"config": peripheral.config}
            )

            return data
        except ValidationError as e:
            errors = {"extra_settings": {}}
            for err in e.errors():
                path = ".".join(str(x) for x in err["loc"])
                errors["extra_settings"][f"{path}"] = err["msg"]
            raise serializers.ValidationError(errors)
