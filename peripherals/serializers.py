from rest_framework import serializers

from dispatcher.command_message.factory import command_message_factory
from dispatcher.processor.action_event_command import action_event_command_processor
from hardware.base import HardwareValidationError
from hardware.registry import HARDWARE_REGISTRY
from peripherals.models import Peripherals
from pydantic import ValidationError

from redis_cache import redis_cache


class PeripheralSerializerDevice(serializers.ModelSerializer):
    class Meta:
        model = Peripherals
        fields = ["id", "name", "config", "state"]


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
        data = PeripheralSerializerDevice(peripheral.device.peripherals, many=True).data
        command_message = command_message_factory.update_peripheral(
            peripheral.device, {"peripherals": data}
        )
        action_event_command_processor(command_message)
        return peripheral
