from rest_framework import serializers

from consumers.router_message.builders.base import build_request
from consumers.router_message.message_event import MessageEvent
from consumers.device.messenger import DeviceMessenger
from hardware.base import HardwareValidationError
from hardware.registry import HARDWARE_REGISTRY
from peripherals.models import Peripherals
from pydantic import ValidationError


class PeripheralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peripherals
        fields = ["id", "name", "device", "config", "state"]

    def validate(self, data):
        Peripherals.objects.all().delete()
        name = data.get("name")
        hardware_cls = HARDWARE_REGISTRY.get(name)
        errors = {}
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

        #
        # if "state" in data:
        #     try:
        #         registry.state_model(**data["state"])
        #     except ValidationError as e:
        #         for err in e.errors():
        #             path = ".".join(str(x) for x in err["loc"])
        #             errors[f"state.{path}"] = err["msg"]
        #     serializer = registry.state_serializer(data=data["state"])
        #     serializer.is_valid(raise_exception=True)

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        peripheral: Peripherals = super().create(validated_data)
        DeviceMessenger().send(
            "1234",
            build_request(
                MessageEvent.UPDATE_CONFIG,
                peripheral.device.mac,
                {peripheral.pk: {"name": peripheral.name, "config": peripheral.config}},
            ),
        )
        return peripheral
