from kombu.utils.scheduling import priority_cycle
from rest_framework import serializers

from hardware.registry import HARDWARE_REGISTRY
from peripherals.models import Peripherals
from pydantic import ValidationError
from django.db.models import Q


class PeripheralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peripherals
        fields = ["id", "name", "device", "config", "state"]

    def validate(self, data):
        name = data.get("name")
        registry = HARDWARE_REGISTRY.get(name)
        errors = {}
        if registry is None:
            raise serializers.ValidationError({"name": "Unknown device type"})

        if "config" in data:
            try:
                registry.config_model(**data["config"])
            except ValidationError as e:
                for err in e.errors():
                    path = ".".join(str(x) for x in err["loc"])
                    errors[f"config.{path}"] = err["msg"]
            serializer = registry.config_serializer(
                data=data["config"], context={"device": data["device"]}
            )
            serializer.is_valid(raise_exception=True)

        if "state" in data:
            try:
                registry.state_model(**data["state"])
            except ValidationError as e:
                for err in e.errors():
                    path = ".".join(str(x) for x in err["loc"])
                    errors[f"state.{path}"] = err["msg"]
            serializer = registry.state_serializer(data=data["state"])
            serializer.is_valid(raise_exception=True)

        if errors:
            raise serializers.ValidationError(errors)
        return data
