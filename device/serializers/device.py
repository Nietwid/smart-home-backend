from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.db.models import Q
from peripherals.serializers.peripheral import PeripheralSerializer
from room.models import Room

from ..models import Device
from redis_cache import redis_cache


class DeviceSerializer(ModelSerializer):
    peripherals = PeripheralSerializer(many=True, read_only=True)
    pending = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ["last_seen", "mac"]

    def get_pending(self, obj: Device):
        return redis_cache.get_device_pending(obj.pk)

    def validate_room(self, value):
        if not value:
            return value

        user = self.context["request"].user
        if not Room.objects.filter(
            Q(user=user) | Q(visibility="PU"), pk=value.pk
        ).exists():
            raise serializers.ValidationError(
                "You do not have permission to assign this room."
            )
        return value
