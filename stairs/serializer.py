from rest_framework import serializers

# from utils.send_set_settings_request import send_set_settings_request
from .models import Stairs


class StairsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stairs
        exclude = ["mac"]

    # def update(self, instance, validated_data):
    #     instance = super().update(instance, validated_data)
    #     send_set_settings_request(instance)
    #     return instance


class StairsSerializerDevice(serializers.ModelSerializer):
    class Meta:
        model = Stairs
        fields = ["brightness", "step", "lighting_time", "light_count"]
