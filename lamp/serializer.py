from rest_framework import serializers

from utils.send_set_settings_request import send_set_settings_request
from .models import Lamp


class LampSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lamp
        exclude = ["mac"]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        send_set_settings_request(instance)
        return instance


class LampSerializerDevice(serializers.ModelSerializer):
    class Meta:
        model = Lamp
        fields = ["brightness", "step", "lighting_time"]
