from rest_framework import serializers

from button.models import ButtonType

# from utils.button_type_change import button_type_change
from utils.send_set_settings_request import send_set_settings_request
from .models import Light


class LightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Light
        exclude = ["mac"]

    def validate_button_type(self, value):
        if value not in [ButtonType.MONOSTABLE, ButtonType.BISTABLE]:
            raise serializers.ValidationError("Wrong button type")
        return value

    # def update(self, instance: Light, validated_data: dict):
    #     if "button_type" in validated_data:
    #         button_type_change(validated_data["button_type"], instance)
    #
    #     response = super().update(instance, validated_data)
    #
    #     if "button_type" in validated_data:
    #         send_set_settings_request(instance)
    #     return response


class LightSerializerDevice(serializers.ModelSerializer):

    class Meta:
        model = Light
        fields = ["button_type"]
