from rest_framework import serializers

from dispatcher.device.messages.enum import MessageCommand
from hardware.base import HardwareValidationError
from hardware.registry import HARDWARE_REGISTRY
from notifier.factory.frontend_notifier_factory import frontend_notifier_factory
from peripherals.models import Peripherals
from peripherals.utils.validate_pydantic_model import validate_pydantic_model

from redis_cache import redis_cache
from typing import Collection
from notifier.notifier import notifier
from device.models import Device


class PeripheralSerializerDevice(serializers.ModelSerializer):
    class Meta:
        model = Peripherals
        fields = ["id", "name", "config", "state"]


class PeripheralSerializer(serializers.ModelSerializer):
    pending = serializers.SerializerMethodField(read_only=True)
    available_event = serializers.SerializerMethodField(read_only=True)
    available_action = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Peripherals
        fields = [
            "id",
            "name",
            "device",
            "config",
            "state",
            "pending",
            "available_event",
            "available_action",
        ]
        read_only_fields = ["pending"]

    def get_available_event(self, obj: Peripherals) -> list[MessageCommand]:
        hardware_cls = HARDWARE_REGISTRY.get(obj.name)
        return hardware_cls.get_available_events()

    def get_available_action(self, obj: Peripherals) -> Collection[MessageCommand]:
        hardware_cls = HARDWARE_REGISTRY.get(obj.name)
        return hardware_cls.get_available_actions()

    def get_pending(self, obj: Peripherals) -> list[str]:
        return redis_cache.get_peripherals_pending(obj.pk)

    def validate(self, data):
        name = data.get("name")
        hardware_cls = HARDWARE_REGISTRY.get(name)
        errors = {}
        if hardware_cls is None:
            raise serializers.ValidationError({"name": "Unknown device type"})

        if "config" in data:
            errs = validate_pydantic_model(
                hardware_cls.config_model,
                data["config"],
                data["device"],
                hardware_cls.validate_config,
            )
            errors.update({f"config.{k}": v for k, v in errs.items()})

        if "state" in data:
            errs = validate_pydantic_model(
                hardware_cls.state_model,
                data["state"],
                data["device"],
                hardware_cls.validate_state,
            )
            errors.update({f"state.{k}": v for k, v in errs.items()})
        elif not self.instance:
            data["state"] = hardware_cls.state_model().model_dump()

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        peripheral: Peripherals = super().create(validated_data)
        device: Device = peripheral.device

        if MessageCommand.UPDATE_PERIPHERAL in device.required_action:
            return peripheral

        device.required_action.append(MessageCommand.UPDATE_PERIPHERAL)
        device.save(update_fields=["required_action"])
        message = frontend_notifier_factory.update_device_required_action(
            device.home.pk, device.required_action, device.pk
        )
        notifier.notify([message])
        return peripheral
