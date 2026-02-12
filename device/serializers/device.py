from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from consumers.frontend_message.messenger import FrontendMessenger
from device_registry import DeviceRegistry
from event.serializer import EventSerializer
from peripherals.serializers import PeripheralsSerializer

from ..models import (
    Device,
)


class DeviceSerializer(ModelSerializer):
    peripherals = PeripheralsSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        exclude = ["mac"]
        read_only_fields = ["last_seen"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        data = EventSerializer(instance.events.all(), many=True).data
        representation["events"] = data
        return representation

    def update(self, instance, validated_data):
        model_class, serializer_class = self._get_device_serializer(instance)
        device = model_class.objects.get(pk=instance.id)
        serializer = serializer_class(
            device,
            data=self.initial_data,
            context=self.context,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        FrontendMessenger().update_frontend(
            instance.home.id, DeviceSerializer(device).data
        )
        return instance

    def create(self, validated_data):
        _, serializer_class = self._get_device_serializer(validated_data)
        serializer = serializer_class(data=self.initial_data, context=self.context)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def _get_device_serializer(self, obj: Device):
        fun: str = obj.fun.lower()
        if not fun:
            raise serializers.ValidationError("Field 'fun' is required.")
        register = DeviceRegistry()
        model_class = register.get_model(fun)
        serializer_class = register.get_serializer(fun)
        if not serializer_class:
            raise serializers.ValidationError(f"Unsupported device type: {fun}")
        return model_class, serializer_class
