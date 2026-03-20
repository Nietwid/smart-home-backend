from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from peripherals.serializers import PeripheralSerializer

from ..models import Device
from redis_cache import redis_cache


class DeviceSerializer(ModelSerializer):
    peripherals = PeripheralSerializer(many=True, read_only=True)
    pending = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ["last_seen"]

    def get_pending(self, obj: Device):
        pending = redis_cache.get_device_pending(obj.pk)
        if not pending:
            return []
        return pending
