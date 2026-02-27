from rest_framework import serializers

from hardware.base import HardwareValidationError
from hardware.registry import HARDWARE_REGISTRY
from peripherals.models import Peripherals
from pydantic import ValidationError

from redis_cache import redis_cache


class PeripheralSerializer(serializers.ModelSerializer):
    pending = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Peripherals
        fields = ["id", "name", "device", "config", "state", "pending"]
        read_only_fields = ["pending"]

    def get_pending(self, obj: Peripherals) -> list[str]:
        pending = redis_cache.get_peripherals_pending(obj.pk)
        if not pending:
            return []
        return pending

    def validate(self, data):
        name = data.get("name")
        hardware_cls = HARDWARE_REGISTRY.get(name)
        errors = {}
        print(data)
        if hardware_cls is None:
            raise serializers.ValidationError({"name": "Unknown device type"})

        if "config" in data:
            try:
                config_cls = hardware_cls.config_model(**data["config"])
                hardware_cls.validate_config(config_cls, data["device"])
            except ValidationError as e:
                for err in e.errors():
                    path = ".".join(str(x) for x in err["loc"])
                    errors[f"config.{path}"] = err["msg"]
            except HardwareValidationError as e:
                errors.update(e.errors)

        if "state" in data:
            try:
                state_cls = hardware_cls.state_model(**data["state"])
                hardware_cls.validate_state(state_cls, data["device"])
            except ValidationError as e:
                for err in e.errors():
                    path = ".".join(str(x) for x in err["loc"])
                    errors[f"state.{path}"] = err["msg"]
            except HardwareValidationError as e:
                errors.update(e.errors)
        elif self.instance is None:
            data["state"] = hardware_cls.state_model().model_dump()
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        peripheral: Peripherals = super().create(validated_data)
        # DeviceMessenger().send(
        #     "1234",
        #     build_request(
        #         MessageEvent.UPDATE_CONFIG,
        #         peripheral.device.mac,
        #         {peripheral.pk: {"name": peripheral.name, "config": peripheral.config}},
        #     ),
        # )
        return peripheral
