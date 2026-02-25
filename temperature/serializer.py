from rest_framework import serializers

from consumers.router_message.builders.basic import set_settings_request
from consumers.router_message.messenger import DeviceMessenger
from utils.waiting_time import waiting_time
from .models import TempHum


class TempHumSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempHum
        exclude = [
            "mac",
            "home",
        ]

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        request = set_settings_request(instance.mac, validated_data)
        DeviceMessenger().send(instance.get_router_mac(), request)
        return instance


class TempHumSerializerDevice(serializers.ModelSerializer):
    waiting_time = serializers.SerializerMethodField()

    def get_waiting_time(self, obj) -> int:
        return waiting_time()

    class Meta:
        model = TempHum
        fields = [
            "waiting_time",
            "temperature_hysteresis",
            "humidity_hysteresis",
            "trigger_temp_up",
            "trigger_temp_down",
            "trigger_hum_up",
            "trigger_hum_down",
        ]
